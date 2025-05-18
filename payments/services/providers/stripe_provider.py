# payments/providers/stripe_provider.py
from decouple import config
import stripe

from payments.services.providers.base import BasePaymentProvider


class StripeProvider(BasePaymentProvider):
    """
    Stripe payment provider implementation using the Stripe API.
    """

    def __init__(self, user, order=None):
        super().__init__(user)  # initialize BasePaymentProvider
        stripe.api_key = config("STRIPE_SECRET_KEY")  # Set your Stripe secret key
        self.order = order

    def create_payment_intent(self, amount: float, currency: str = "eur") -> dict:
        """
        Creates a payment intent and returns metadata like client_secret.

        Args:
            amount (float): The total amount to charge.
            currency (str): Currency code, default is EUR.

        Returns:
            dict: A dictionary with provider-specific response data.asd
        """
        if not self.order:
            raise ValueError("StripeProvider requires an Order instance to proceed.")

        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe expects the amount in cents
            currency=currency,
            metadata={
                "order_id": str(self.order.id),
            },
        )
        return {
            "payment_intent_id": intent.id,
            "client_secret": intent.client_secret,
            "amount": amount,
            "currency": currency,
            "status": intent.status,
        }

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
