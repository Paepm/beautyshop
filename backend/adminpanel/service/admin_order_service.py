from orders.models import Order
from adminpanel.serializers.serializers import AdminOrderSerializer


class AdminOrderService:
    def __init__(self):
        pass

    def get_all_orders(self) -> AdminOrderSerializer:

        orders = Order.objects.all().order_by("-created_at")
        serializer = AdminOrderSerializer(orders, many=True)

        return serializer
