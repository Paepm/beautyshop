from django.core.exceptions import ObjectDoesNotExist

from orders.models import Order
from backend.orders.services.order_status_service import OrderStatusService
from orders.enums.paymentstatus import PaymentStatus


class OrderService:
    def __init__(self, user, request):
        self.user = user
        self.request = request
        self.session = request.session

    def get_existing_open_order(self) -> Order | None:
        order_id = self.session.get("order_id")
        if not order_id:
            return None

        try:
            return Order.objects.get(
                id=order_id,
                user=self.user,
                payment_status=PaymentStatus.OPEN,
            )
        except ObjectDoesNotExist:
            return None

    def process_order(
        self, payment_provider=None, shipping_data=None, shipping_method="standard"
    ) -> Order | None:
        creator = OrderStatusService(self.user)
        return creator.create_order(
            payment_provider=payment_provider,
            shipping_data=shipping_data,
            shipping_method=shipping_method,
        )
