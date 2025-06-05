from orders.models import Order, OrderItem


class OrderViewService:
    @staticmethod
    def get_user_orders(user):
        return Order.objects.filter(user=user).order_by("-created_at")

    @staticmethod
    def get_user_order(user, order_id):
        try:
            return Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_order_items(order_id):
        return OrderItem.objects.filter(order__id=order_id)
