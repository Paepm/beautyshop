from orders.models import Order
from orders.serializer.serializer import OrderSerializer


class AdminOrderService:
    def __init__(self):
        pass

    def get_all_orders(self) -> OrderSerializer:

        orders = Order.objects.all().order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)

        return serializer
