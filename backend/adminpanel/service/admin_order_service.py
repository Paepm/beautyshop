from django.utils.dateparse import parse_date
from devtools import debug
from rest_framework.exceptions import NotFound

from orders.models import Order
from adminpanel.serializers.serializers import AdminOrderSerializer


class AdminOrderService:

    def get_all_orders(self, filters=None) -> AdminOrderSerializer:
        orders = self.get_queryset(filters)
        serializer = AdminOrderSerializer(orders, many=True)
        return serializer.data

    def get_order_by_id(self, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = AdminOrderSerializer(order)
            return serializer.data
        except Order.DoesNotExist:
            return None

    def get_queryset(self, filters):
        orders = Order.objects.all().order_by("-created_at")

        if filters:
            payment_status = filters.get("payment_status")
            order_status = filters.get("order_status")
            date_from = filters.get("date_from")
            date_to = filters.get("date_to")
            username = filters.get("username")

            if payment_status:
                orders = orders.filter(payment_status=payment_status)
            if order_status:
                orders = orders.filter(order_status=order_status)
            if date_from:
                orders = orders.filter(created_at__date__gte=parse_date(date_from))
            if date_to:
                orders = orders.filter(created_at__date__lte=parse_date(date_to))
            if username:
                orders = orders.filter(user__username__icontains=username)

        return orders

    def update_order_and_tracking_status(
        self,
        pk,
        new_order_status,
        new_shipping_provider=None,
        new_tracking_id=None,
        new_tracking_url=None,
    ):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise NotFound("Order not found")

        if new_order_status is not None:
            order.order_status = new_order_status

        if new_shipping_provider is not None:
            order.shipping_provider = new_shipping_provider

        if new_tracking_id is not None:
            order.tracking_id = new_tracking_id

        if new_tracking_url is not None:
            order.tracking_url = new_tracking_url

        order.save()

        return AdminOrderSerializer(order).data
