from orders.services.order_creator import OrderCreator
from orders.models import Order
from django.core.exceptions import ObjectDoesNotExist


class OrderService:
    def __init__(self, user, request):
        self.user = user
        self.request = request
        self.session = request.session

    def get_existing_open_order(self) -> Order | None:
        """
        Checks the session for an existing open order. Returns the order if valid.
        """
        order_id = self.session.get("order_id")
        if not order_id:
            return None

        try:
            order = Order.objects.get(
                id=order_id, user=self.user, payment_status=Order.PaymentStatus.OPEN
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
