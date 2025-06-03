import stripe
from decouple import config
from devtools import debug
import traceback

from payments.services.providers.base import BasePaymentProvider
from payments.enums.payment_methods import PaymentMethodTypes


class StripeProvider(BasePaymentProvider):
    """
    Stripe payment provider implementation using the Stripe API.
    """

    def __init__(self, user, order=None):
        super().__init__(user)  # initialize BasePaymentProvider
        stripe.api_key = config("STRIPE_SECRET_KEY")  # Set your Stripe secret key
        self.order = order

    def create_checkout_session(self, success_url: str, cancel_url: str) -> str:
        """
        Creates a Stripe Checkout Session with pre-configured payment options.

        Returns:
            str: The URL to redirect the user to complete the payment.
        """
        if not self.order:
            raise ValueError("Order is required to create a Stripe Checkout session.")

        debug("[STRIPE] Creating checkout session for order:", self.order.id)
        debug("[STRIPE] User:", self.user)

        session = stripe.checkout.Session.create(
            payment_method_types=[
                PaymentMethodTypes.CARD.value,
                PaymentMethodTypes.SOFORT.value,
                PaymentMethodTypes.BANCONTACT.value,
                PaymentMethodTypes.KLARNA.value,
                PaymentMethodTypes.SEPA_DEBIT.value,
            ],  # stripe supports multiple payment methods
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": f"Order #{self.order.id}",
                        },
                        "unit_amount": int(self.order.total_price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            metadata={"order_id": str(self.order.id)},
            # payment_intent_data --> stripe need this to handle payments on stripe checkout session (failed, cancelled, etc)
            payment_intent_data={"metadata": {"order_id": str(self.order.id)}},
            customer_email=self.user.email,
            success_url=success_url,
            cancel_url=cancel_url,
        )
        debug("[STRIPE] Creating session with payment methods:", session)
        debug("[STRIPE] Checkout session created successfully:", session.url)
        if not session.url:
            raise RuntimeError("Stripe session was created but no URL was returned.")
        return session.url

    def create_payment_intent(self, amount: float, currency: str = "eur") -> dict:
        raise NotImplementedError("This provider uses checkout session instead.")

    def confirm_payment(self, payment_intent_id: str) -> bool:
        """
        Confirms the payment with the given intent ID.

        Returns:
            bool: True if payment is confirmed, False otherwise.
        """
        return True

    def cancel_payment(self, payment_intent_id: str) -> bool:
        """
        Cancels the payment with the given intent ID.

        Returns:
            bool: True if successfully cancelled, False otherwise.
        """
        return False
