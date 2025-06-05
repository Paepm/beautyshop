import stripe
from decouple import config
from devtools import debug

from payments.services.providers.base import BasePaymentProvider
from payments.enums.payment_methods import PaymentMethodTypes


class StripeProvider(BasePaymentProvider):
    """
    Stripe payment provider implementation using the Stripe API.
    """

    def __init__(self, user, order=None):
        super().__init__(user)
        stripe.api_key = config("STRIPE_SECRET_KEY")
        self.order = order

    def create_checkout_session(self, success_url: str, cancel_url: str) -> str:
        """
        Create a Stripe Checkout Session and return the redirect URL.

        Args:
            success_url (str): URL to redirect after successful payment.
            cancel_url (str): URL to redirect if user cancels.

        Returns:
            str: URL to redirect user to Stripe Checkout.
        """
        if not self.order:
            raise ValueError("Order is required to create a Stripe Checkout session.")

        debug(f"[STRIPE] Creating checkout session for Order #{self.order.id}")
        debug(f"[STRIPE] User: {self.user.email}")

        session = stripe.checkout.Session.create(
            payment_method_types=[
                PaymentMethodTypes.CARD.value,
                PaymentMethodTypes.SOFORT.value,
                PaymentMethodTypes.BANCONTACT.value,
                PaymentMethodTypes.KLARNA.value,
                PaymentMethodTypes.SEPA_DEBIT.value,
            ],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {"name": f"Order #{self.order.id}"},
                        "unit_amount": int(
                            self.order.total_price * 100
                        ),  # Stripe expects cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            metadata={"order_id": str(self.order.id)},
            payment_intent_data={"metadata": {"order_id": str(self.order.id)}},
            customer_email=self.user.email,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        debug("[STRIPE] Checkout session created:", session.id)

        if not session.url:
            raise RuntimeError("Stripe session was created but no URL was returned.")

        return session.url

    def create_payment_intent(self, amount: float, currency: str = "eur") -> dict:
        raise NotImplementedError("This provider uses checkout sessions instead.")

    def confirm_payment(self, payment_intent_id: str) -> bool:
        """
        Stripe handles confirmation in checkout sessions; this is a placeholder.
        """
        return True

    def cancel_payment(self, payment_intent_id: str) -> bool:
        """
        Stripe handles cancellation externally; this is a placeholder.
        """
        return False
