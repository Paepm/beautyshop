from devtools import debug
from django.utils.timezone import now
from orders.models import Order
from orders.enums.paymentstatus import PaymentStatus
from backend.orders.services.old_order_service import OrderService
from payments.services.payment_service import PaymentService


class StripeWebhookHandler:
    def __init__(self, request):
        self.request = request

    def handle(self, event) -> str:
        event_type = event["type"]
        method_name = f'handle_{event_type.replace(".", "_")}'
        debug(f"[HANDLE] Dispatching method: {method_name}")

        method = getattr(self, method_name, self.handle_default)
        return method(event)

    def handle_checkout_session_completed(self, event) -> str:
        session = event["data"]["object"]
        debug(f"[COMPLETED] Session received: {session}")

        order_id = session.get("metadata", {}).get("order_id")
        if not order_id:
            debug("[COMPLETED] No order_id in metadata.")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[COMPLETED] Order {order_id} not found.")
            return "Ignored"

        if order.payment_status == PaymentStatus.PAID:
            debug(f"[COMPLETED] Order {order_id} already marked as PAID.")
            return "Already paid"

        OrderService(order.user, self.request, order).set_paid()
        debug(f"[COMPLETED] Order {order_id} marked as PAID.")

        payment_intent_id = session.get("payment_intent")
        if payment_intent_id:
            PaymentService(
                order.user
            ).store_payment_method_from_stripe_intent_and_save_in_order(
                order, payment_intent_id
            )

        return "Handled: checkout.session.completed"

    def handle_payment_intent_payment_failed(self, event) -> str:
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")
        if not order_id:
            debug("[FAILED] No order_id in metadata")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[FAILED] Order {order_id} not found")
            return "Ignored"

        if order.payment_status == PaymentStatus.OPEN:
            OrderService(order.user, self.request, order).set_payment_failed()
            debug(f"[FAILED] Order {order_id} marked as FAILED.")

        payment_intent_id = intent.get("id")
        if payment_intent_id:
            try:
                PaymentService(
                    order.user
                ).store_payment_method_from_stripe_intent_and_save_in_order(
                    order, payment_intent_id
                )
            except Exception as e:
                debug(f"[FAILED] Couldn't save payment method: {e}")

        return "Handled: payment_intent.payment_failed"

    def handle_payment_intent_canceled(self, event) -> str:
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")

        if not order_id:
            debug("[CANCELED] No order_id in metadata")
            return "Ignored"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[CANCELED] Order {order_id} not found")
            return "Ignored"

        if order.payment_status == PaymentStatus.OPEN:
            OrderService(order.user, self.request, order).set_payment_cancelled()
            debug(f"[CANCELED] Order {order_id} marked as CANCELED")

        return "Handled: payment_intent.canceled"

    def handle_default(self, event) -> str:
        debug(f"[DEFAULT] Unhandled Stripe event type: {event['type']}")
        return "Ignored"
