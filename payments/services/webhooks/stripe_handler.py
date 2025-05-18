from devtools import debug
import pdb

from orders.models import Order


class StripeWebhookHandler:

    def __init__(self, request):
        self.request = request

    def handle(self, event) -> str:
        """
        Dispatches a Stripe event to its corresponding handler method.

        This method dynamically maps the Stripe event type (e.g., "payment_intent.succeeded")
        to a corresponding handler method (e.g., `handle_payment_intent_succeeded`). If no
        matching handler method is found, the default handler (`handle_default`) is called.

        Args:
            event (dict): The Stripe event payload.

        Returns:
            str: A response message from the executed handler.
        """
        event_type = event["type"]
        method_name = f'handle_{event_type.replace(".", "_")}'
        debug(f"[HANDLE]: Looking for handler method: {method_name}")

        method = getattr(self, method_name, self.handle_default)
        return method(event)

    # function naming should be like: handle_{event_type}
    def handle_payment_intent_succeeded(self, event) -> str:
        pdb.set_trace()

        intent = event["data"]["object"]
        debug(f"Stripe_intent:", intent)

        user_id = intent["metadata"].get("user_id")
        debug(f"User_id {user_id}!")

        # logic to handle successful payment
        if user_id:
            try:
                order = Order.objects.filter(
                    user_id=user_id, payment_status="open"
                ).latest("created_at")
                debug("order:", order)
                order.payment_status = "paid"
                debug("order_status:", order.payment_status)
                order.save()
            except Order.DoesNotExist:
                debug(f"No open order found for user {user_id}.")
        else:
            debug("No user ID found in metadata.")

        debug(f"Payment succeeded for user {user_id}!")

        return "Handled: payment_intent.succeeded"

    # function naming should be like: handle_{event_type}
    def handle_payment_intent_payment_failed(self, event) -> str:
        intent = event["data"]["object"]
        user_id = intent["metadata"].get("user_id")
        error_message = intent.get("last_payment_error", {}).get(
            "message", "Unknown error"
        )

        debug(f"Payment failed: {user_id} - {error_message}")

        # logic to handle failed payment
        if user_id:
            try:
                order = Order.objects.filter(
                    user_id=user_id, payment_status="open"
                ).latest("created_at")
                order.payment_status = "failed"
                order.save()
                debug("order_status:", order.payment_status)
            except Order.DoesNotExist:
                debug(f"No open order found for user {user_id}.")
        else:
            debug("No user ID found in metadata.")

        return "Handled: payment_intent.payment_failed"

    def handle_default(self, event) -> str:
        """
        Default handler for unrecognized Stripe event types.

        This method is called when no specific handler exists for the received
        Stripe event. It logs the event type for debugging purposes and returns
        a simple response message.

        Args:
            event (dict): The Stripe event payload that was not matched.

        Returns:
            str: A response message indicating the event was ignored.
        """
        debug(f"[HANDLE_DEFAULT]: Unhandled event type: {event['type']}")
        return "Ignored"
