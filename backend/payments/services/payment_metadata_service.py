# payments/services/payment_metadata_service.py

import stripe
from django.conf import settings
from orders.models import Order
from devtools import debug


class PaymentMetadataService:
    """
    Service to extract metadata (e.g. used payment method) from Stripe PaymentIntent
    and persist it in the related Order.
    """

    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def save_method_from_stripe_intent(
        self, order: Order, payment_intent_id: str
    ) -> None:
        """
        Retrieves the Stripe PaymentIntent and stores the used payment method in the order.

        Args:
            order (Order): The related order to update.
            payment_intent_id (str): The Stripe payment intent ID from the session.
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            method_list = intent.get("payment_method_types", [])

            if method_list:
                method = method_list[0]
                order.payment_method = method
                order.save(update_fields=["payment_method"])
                debug(
                    f"[PAYMENT_METADATA] Saved method '{method}' to order #{order.id}"
                )
            else:
                debug(
                    f"[PAYMENT_METADATA] No method found for intent {payment_intent_id}"
                )

        except Exception as e:
            debug(f"[PAYMENT_METADATA] Failed to fetch or save payment method: {e}")
