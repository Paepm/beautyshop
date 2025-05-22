from devtools import debug
from django.conf import settings
import stripe

from orders.models import Order
from payments.services.provider_registry import PROVIDER_MAP
from payments.enums.payment_providers import PaymentProviders


class PaymentService:
    """Handles supported payment providers and initiates checkout flows."""

    def __init__(self, user):
        """
        Initialize the PaymentService with the current user.

        Args:
            user (CustomUser): The authenticated user for whom the service acts.
        """
        self.user = user

    def validate_payment_provider(self, provider: str) -> bool:
        """
        Check if the provided payment provider is supported.

        Args:
            provider (str): The payment provider to validate (e.g. 'stripe', 'paypal').

        Returns:
            bool: True if supported, False otherwise.
        """
        try:
            PaymentProviders(provider)
            return True
        except ValueError:
            return False

    def save_payment_provider_to_order(self, order: Order, provider: str) -> None:
        """
        Save the selected payment provider (e.g. 'stripe', 'paypal') to the order.

        Args:
            order (Order): The order instance to update.
            provider (str): The selected payment provider.

        Raises:
            ValueError: If the provider is not supported.
        """
        if not self.validate_payment_provider(provider):
            raise ValueError(f"Invalid payment provider: {provider}")

        order.payment_provider = provider
        order.save()

    def get_supported_payment_providers(self) -> list[str]:
        """
        Return all supported payment providers.

        Returns:
            list[str]: A list of valid payment provider strings (e.g. ['stripe', 'paypal']).
        """
        return [provider.value for provider in PaymentProviders]

    def process_payment(
        self, provider_key: str, order: Order, success_url=None, cancel_url=None
    ) -> dict:
        """
        Create a checkout session with the selected payment provider.

        Args:
            provider_key (str): The identifier of the provider (e.g. 'stripe', 'paypal').
            order (Order): The order to be paid.
            success_url (str): URL to redirect after successful payment.
            cancel_url (str): URL to redirect if payment is cancelled.

        Returns:
            dict: A result dictionary with status and redirect URL or error message.
        """
        provider_class = PROVIDER_MAP.get(provider_key)
        if not provider_class:
            return {"status": "unsupported", "message": "Unsupported provider."}

        provider = provider_class(self.user, order)

        if hasattr(provider, "create_checkout_session"):
            url = provider.create_checkout_session(success_url, cancel_url)
            return {"status": "ok", "redirect_url": url}

        return {
            "status": "unsupported",
            "message": "Provider does not support checkout.",
        }

    def store_payment_method_from_stripe_intent_and_save_in_order(
        self, order: Order, payment_intent_id: str
    ) -> None:
        """
        Retrieves the Stripe PaymentIntent and stores the used payment method in the order.

        Args:
            order (Order): The related order to update.
            payment_intent_id (str): The Stripe payment intent ID from the session.
        """

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            method_list = intent.get("payment_method_types", [])
            if method_list:
                used_method = method_list[0]
                order.payment_method = used_method
                order.save()
                debug(
                    f"[PAYMENT SERVICE] Stored payment method '{used_method}' in order {order.id}"
                )
            else:
                debug(
                    f"[PAYMENT SERVICE] No payment method found for PaymentIntent {payment_intent_id}"
                )
        except Exception as e:
            debug(f"[PAYMENT SERVICE] Stripe intent fetch failed: {e}")
