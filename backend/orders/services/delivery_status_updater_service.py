from django.utils import timezone
from orders.models import Order


class DeliveryStatusUpdater:
    """
    Checks all shipped orders and marks them as delivered if they are ready for delivery.
    """

    def run(self):
        shipped_orders = Order.objects.filter(
            order_status="shipped", delivered_at__isnull=True
        )

        for order in shipped_orders:
            if order.is_ready_for_delivery_mark():
                order.order_status = "delivered"
                order.delivered_at = timezone.now()
                order.save()
                print(f"Order #{order.id} marked as delivered.")
            else:
                print(f"Order #{order.id} not ready for delivery status.")
