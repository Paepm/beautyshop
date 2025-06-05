from backend.orders.services.old_order_creator_serive import OrderCreatorService
from orders.models import Order
from django.core.exceptions import ObjectDoesNotExist
from devtools import debug

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

    def process_order(
        self, payment_provider=None, shipping_data=None, shipping_method="standard"
    ):
        creator = OrderCreatorService(self.user)
        return creator.create_order(
            payment_provider=payment_provider,
            shipping_data=shipping_data,
            shipping_method=shipping_method,
        )

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
        self.order.order_status = OrderStatus.PROCESSING
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
        self.order.order_status = OrderStatus.PROCESSING
        self.order.save()

    def set_payment_cancelled(self) -> None:
        """ "
        Sets the order payment status to cancelled.
        Args:
            order (Order): The order to update.
        Returns:
            None
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return

        self.order.payment_status = PaymentStatus.FAILED
        self.order.order_status = OrderStatus.CANCELLED
        self.order.save()
