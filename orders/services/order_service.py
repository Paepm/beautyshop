from .order_creator import OrderCreator
from orders.models import Order


# need this class later, for external integrations!
class OrderService:
    def __init__(self, user):
        self.user = user

    def process_order(self, method: str, request) -> Order:
        """
        Return an existing open order or create a new one.

        Saves the order ID into the session.
        """
        order = None
        order_id = request.session.get("order_id")

        if order_id:
            try:
                order = Order.objects.get(
                    id=order_id, payment_status=Order.PaymentStatus.OPEN
                )
            except Order.DoesNotExist:
                pass  # fallback to create below

        if not order:
            order = OrderCreator(self.user).create_order(payment_method=method)
            request.session["order_id"] = order.id

        return order
