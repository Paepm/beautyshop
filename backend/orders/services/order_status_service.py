from orders.models import Order, PaymentStatus, OrderStatus


class OrderStatusService:
    """
    Service for managing order payment statuses.
    Used in payments sector to handle order status after payment events.
    """

    def __init__(self, order):
        self.order: Order = order

    def set_paid(self):
        """
        Set the order payment status to PAID and update the order status to PROCESSING.
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return

        self.order.payment_status = PaymentStatus.PAID
        self.order.order_status = OrderStatus.PROCESSING
        self.order.save()

    def set_payment_failed(self):
        """
        Set the order payment status to FAILED and update the order status to FAILED.
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return
        self.order.payment_status = PaymentStatus.FAILED
        self.order.order_status = OrderStatus.FAILED
        self.order.save()

    def set_payment_processing(self):
        """
        Set the order payment status to PROCESSING and update the order status to PROCESSING.
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return
        self.order.payment_status = PaymentStatus.PROCESSING
        self.order.order_status = OrderStatus.PROCESSING
        self.order.save()

    def set_payment_cancelled(self):
        """
        Set the order payment status to FAILED and update the order status to CANCELLED.
        """
        if self.order.payment_status == PaymentStatus.PAID:
            return
        self.order.payment_status = PaymentStatus.FAILED
        self.order.order_status = OrderStatus.CANCELLED
        self.order.save()
