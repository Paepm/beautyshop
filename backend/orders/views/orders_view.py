from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from devtools import debug

from ..serializer.serializer import OrderSerializer, OrderItemSerializer
from orders.services.orders_view_service import OrderViewService


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = OrderViewService.get_user_orders(request.user).order_by("-created_at")
        debug(f"[ORDER_LIST_VIEW] orders: {orders}")
        serializer = OrderSerializer(orders, many=True)
        debug(f"[ORDER_LIST_VIEW] serialized data: {serializer.data}")

        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = OrderViewService.get_user_order(request.user, order_id)
            debug(f"[ORDER_DETAIL_VIEW] order: {order}")
            serializer = OrderSerializer(order)
            debug(f"[ORDER_DETAIL_VIEW] serialized data: {serializer.data}")
            return Response(serializer.data)
        except order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)


class OrderProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order_items = OrderViewService.get_order_items(order_id=order_id)
            debug(f"[ORDER_PRODUCT_DETAIL_VIEW] order_items: {order_items}")
            serializer = OrderItemSerializer(order_items, many=True)
            debug(f"[ORDER_PRODUCT_DETAIL_VIEW] serialized data: {serializer.data}")
            return Response(serializer.data)
        except order_items.DoesNotExist:
            return Response({"error": "Order items not found"}, status=404)
