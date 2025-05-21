# payments/services/webhooks/stripe_handler.py

from devtools import debug
from django.utils.timezone import now

from orders.models import Order
from orders.enums.paymentstatus import PaymentStatus
from orders.services.order_service import OrderService


class StripeWebhookHandler:
    """
    Handles incoming Stripe webhook events and dispatches them to
    the appropriate method based on event type.

    This handler is designed specifically for the Stripe Checkout Session flow.
    """

    def __init__(self, request):
        """
        Initialize the handler with the current HTTP request context.

        Args:
            request (HttpRequest): The Django request object, used for context (e.g., logging, user access).
        """
        self.request = request

    def handle(self, event) -> str:
        """
        Main entry point for processing a Stripe webhook event.

        Args:
            event (dict): The full Stripe event payload.

        Returns:
            str: A status message indicating how the event was handled.
        """
        event_type = event["type"]
        method_name = f'handle_{event_type.replace(".", "_")}'
        debug(f"[HANDLE]: Looking for handler method: {method_name}")

        method = getattr(self, method_name, self.handle_default)
        return method(event)

    def handle_checkout_session_completed(self, event) -> str:
        """
        Handles the 'checkout.session.completed' event from Stripe.

        This event is sent after a successful payment through a Stripe Checkout Session.
        It updates the order's payment and order status accordingly.

        Args:
            event (dict): The Stripe event payload.

        Returns:
            str: Result message for logging/debugging.
        """
        session = event["data"]["object"]
        order_id = session["metadata"].get("order_id")

        debug(f"[WEBHOOK] checkout.session.completed at {now()}")

        if not order_id:
            debug("❌ No order_id found in session metadata.")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"❌ Order {order_id} not found in database.")
            return "Ignored"

        if order.payment_status == PaymentStatus.PAID:
            debug(f"⏭️ Order {order_id} already marked as PAID.")
            return "Already paid"

        order_service = OrderService(order.user, self.request, order)
        order_service.set_paid()
        debug(f"✅ Order {order_id} marked as PAID + PROCESSING")

        return "Handled: checkout.session.completed"

    def handle_payment_intent_payment_failed(self, event) -> str:
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")

        if not order_id:
            debug("[FAILED] No Order ID in metadata")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[FAILED] Order {order_id} not found")
            raise Exception("Order not found yet")

        if order.payment_status == PaymentStatus.OPEN:
            OrderService(order.user, self.request, order).set_payment_failed()
            debug(f"[FAILED] Set order {order_id} to FAILED")
        else:
            debug(f"[SKIP] Order {order_id} already handled")

        return "Handled: payment_intent.payment_failed"

    def handle_default(self, event) -> str:
        """
        Default fallback handler for unrecognized or unused event types.

        Args:
            event (dict): The Stripe event payload.

        Returns:
            str: Always returns 'Ignored'.
        """
        debug(f"[HANDLE_DEFAULT]: Unhandled event type: {event['type']}")
        return "Ignored"
