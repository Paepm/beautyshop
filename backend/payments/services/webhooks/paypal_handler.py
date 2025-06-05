from devtools import debug
import requests

from orders.models import Order
from orders.enums.paymentstatus import PaymentStatus
from orders.enums.orderstatus import OrderStatus
from backend.orders.services.old_order_service import OrderService
from payments.services.providers.paypal_provider import PayPalProvider


class PayPalWebhookHandler:
    def __init__(
        self,
        request,
    ):
        self.request = request
        self.access_token = PayPalProvider(request.user).access_token

    def handle(self, event: dict) -> str:
        """
        Dispatch PayPal event to matching handler.
        """
        event_type = event.get("event_type")
        debug(f"[PAYPAL HANDLE] Received event: {event_type}")
        method_name = f"handle_{event_type.replace('.', '_')}"

        method = getattr(self, method_name, self.handle_default)
        return method(event)

    def handle_CHECKOUT_ORDER_APPROVED(self, event: dict) -> str:
        """
        Called when a PayPal Checkout Order was approved by user.

        This is triggered after user approval but *before* the money is captured.
        You can initiate the capture here manually using PayPal API.
        """
        debug("[PAYPAL APPROVED]", event)
        order_id = self._get_order_id_from_event(event)

        if not order_id:
            return "Ignored – no order_id"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return f"Order {order_id} not found."

        if order.payment_status == PaymentStatus.PAID:
            return "Already paid."

        # STEP 1: Get capture URL from event (it’s in the 'links' list)
        resource = event.get("resource", {})
        capture_url = None
        for link in resource.get("links", []):
            if link.get("rel") == "capture":
                capture_url = link.get("href")
                break

        if not capture_url:
            return "Capture URL not found."

        # STEP 2: Use the access token already available in the procvider instance
        token = self.access_token

        # STEP 3: Capture the payment
        response = requests.post(
            capture_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        if response.status_code != 201:
            debug("[PAYPAL] Capture failed:", response.json())
            return "Capture failed"

        # STEP 4: Mark order as paid
        OrderService(order.user, self.request, order).set_payment_processing()
        debug(f"[PAYPAL] Order {order_id} captured and marked as processing")

        return "Handled: CHECKOUT.ORDER.APPROVED (with capture)"

    def handle_PAYMENT_CAPTURE_COMPLETED(self, event: dict) -> str:
        """
        Called when a PayPal payment has been successfully captured.
        This is the final confirmation that the funds were transferred.

        Args:
                event (dict): The PayPal event payload.

        Returns:
            str: Result message.
        """
        debug("[PAYPAL CAPTURE COMPLETED]", event)
        order_id = self._get_order_id_from_event(event)
        if not order_id:
            return "Ignored – no order_id"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return f"Order {order_id} not found."

        if order.payment_status == PaymentStatus.PAID:
            return "Already marked as paid"

        # STEP 5: this payment_method is hardcoded, because for paypal provider is only the paypal payment_method useable -> and save updated order
        order.payment_method = "paypal"
        order.save(update_fields=["payment_method"])

        # STEP 6: Set order as paid
        OrderService(order.user, self.request, order).set_paid()
        debug(f"[PAYPAL] Order {order_id} marked as PAID after capture")

        return "Handled: PAYMENT.CAPTURE.COMPLETED"

    def handle_PAYMENT_CAPTURE_DENIED(self, event: dict) -> str:
        debug("[PAYPAL DENIED]", event)

        order_id = self._get_order_id_from_event(event)
        if not order_id:
            debug(["PAYPAL DENIED] No order_id found in event"])
            return "Ignored – no order_id"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            debug(f"[PAYPAL DENIED] Order {order_id} not found.")
            return "Order not found"

        if order.payment_status != PaymentStatus.FAILED:
            order.payment_method = "paypal"
            OrderService(order.user, self.request, order).set_payment_failed()
            debug(f"[PAYPAL DENIED] Order {order_id} marked as FAILED.")

        else:
            debug(f"[PAYPAL DENIED] Order {order_id} was already FAILED.")

        return "Handled: PAYMENT.CAPTURE.DENIED"

    def handle_default(self, event: dict) -> str:
        debug(f"[PayPal] No handler for event type: {event.get('event_type')}")
        return "Ignored"

    def _get_order_id_from_event(self, event: dict) -> str | None:
        """
        Extracts the custom order ID from the PayPal webhook payload.
        Tries multiple locations depending on the event structure.
        """
        try:
            # Normalfall bei CHECKOUT.ORDER.APPROVED
            return event["resource"]["purchase_units"][0]["custom_id"]
        except (KeyError, IndexError, TypeError):
            pass

        try:
            # Fallback: capture-Events enthalten es manchmal direkt
            return event["resource"]["custom_id"]
        except KeyError:
            pass

        debug("No custom_id found in event payload.")
        return None
