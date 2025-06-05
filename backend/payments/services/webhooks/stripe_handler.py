from devtools import debug
from orders.models import Order
from orders.enums.paymentstatus import PaymentStatus

from orders.services.order_status_service import OrderStatusService
from payments.services.payment_metadata_service import PaymentMetadataService
from cart.services.cart_services import CartService


class StripeWebhookHandler:
    def __init__(self, request):
        self.request = request

    def handle(self, event) -> str:
        event_type = event["type"]
        method_name = f"handle_{event_type.replace('.', '_')}"
        debug(f"[STRIPE_WEBHOOK] Dispatching method: {method_name}")
        method = getattr(self, method_name, self.handle_default)
        return method(event)

    def handle_checkout_session_completed(self, event) -> str:
        session = event["data"]["object"]
        debug(f"[STRIPE_COMPLETED] Session received: {session}")

        order_id = session.get("metadata", {}).get("order_id")
        if not order_id:
            debug("[STRIPE_COMPLETED] No order_id in metadata.")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[STRIPE_COMPLETED] Order {order_id} not found.")
            return "Ignored"

        if order.payment_status == PaymentStatus.PAID:
            debug(f"[STRIPE_COMPLETED] Order {order_id} already marked as PAID.")
            return "Already paid"

        OrderStatusService(order).set_paid()
        debug(f"[STRIPE_COMPLETED] Order {order_id} marked as PAID.")

        # Clear the cart after successful payment
        CartService(order.user).clear_cart()

        payment_intent_id = session.get("payment_intent")
        if payment_intent_id:
            PaymentMetadataService().save_method_from_stripe_intent(
                order, payment_intent_id
            )

        return "Handled: checkout.session.completed"

    def handle_payment_intent_payment_failed(self, event) -> str:
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")
        if not order_id:
            debug("[STRIPE_FAILED] No order_id in metadata")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[STRIPE_FAILED] Order {order_id} not found")
            return "Ignored"

        if order.payment_status == PaymentStatus.OPEN:
            OrderStatusService(order).set_payment_failed()
            debug(f"[STRIPE_FAILED] Order {order_id} marked as FAILED.")

        payment_intent_id = intent.get("id")
        if payment_intent_id:
            try:
                PaymentMetadataService().save_method_from_stripe_intent(
                    order, payment_intent_id
                )
            except Exception as e:
                debug(f"[STRIPE_FAILED] Error saving payment method: {e}")

        return "Handled: payment_intent.payment_failed"

    def handle_payment_intent_canceled(self, event) -> str:
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")

        if not order_id:
            debug("[STRIPE_CANCELED] No order_id in metadata")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[STRIPE_CANCELED] Order {order_id} not found")
            return "Ignored"

        if order.payment_status == PaymentStatus.OPEN:
            OrderStatusService(order).set_payment_cancelled()
            debug(f"[STRIPE_CANCELED] Order {order_id} marked as CANCELED")

        return "Handled: payment_intent.canceled"

    def handle_default(self, event) -> str:
        debug(f"[STRIPE_DEFAULT] Unhandled event type: {event['type']}")
        return "Ignored"
