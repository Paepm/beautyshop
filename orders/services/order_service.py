from orders.services.order_creator import OrderCreator
from orders.models import Order
from django.core.exceptions import ObjectDoesNotExist

from orders.enums.paymentstatus import PaymentStatus
from orders.enums.orderstatus import OrderStatus


class OrderService:
    def __init__(self, user, request, order=None):
        self.user = user
        self.request = request
        self.session = request.session
        self.order = order

    def get_existing_open_order(self) -> Order | None:
        """
        Checks the session for an existing open order. Returns the order if valid.
        """
        order_id = self.session.get("order_id")
        if not order_id:
            return None

        try:
            order = Order.objects.get(
                id=order_id, user=self.user, payment_status=PaymentStatus.OPEN
            )
            return order
        except ObjectDoesNotExist:
            return None

    def process_order(self, payment_method: str) -> Order:
        """
        Returns an existing open order from session or creates a new one.

        Also updates the session with the current order ID.
        """
        existing_order = self.get_existing_open_order()
        if existing_order:
            return existing_order

        new_order = OrderCreator(self.user).create_order(payment_method=payment_method)
        self.session["order_id"] = new_order.id
        return new_order

    def set_paid(self) -> None:
        """ "
        Sets the order payment status to paid and updates the order status to processing.
        Args:
            order (Order): The order to update.
        Returns:
            None
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return  # Already paid

        self.order.payment_status = PaymentStatus.PAID
        self.order.order_status = (
            OrderStatus.PROCESSING
        )  # automatically set to processing
        self.order.save()

    def set_payment_failed(self) -> None:
        """ "
        Sets the order payment status to failed and updates the order status to cancelled.
        Args:
            order (Order): The order to update.
        Returns:
            None
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return

        self.order.payment_status = PaymentStatus.FAILED
        self.order.order_status = OrderStatus.FAILED
        self.order.save()

    def set_payment_processing(self) -> None:
        """ "
        Sets the order payment status to processing.
        Args:
            order (Order): The order to update.
        Returns:
            None
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return

        self.order.payment_status = PaymentStatus.PROCESSING
        self.order.save()
