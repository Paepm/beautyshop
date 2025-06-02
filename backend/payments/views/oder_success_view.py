from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializer.serializer import OrderSerializer


class OrderSuccessView(APIView):
    """
    View to handle successful order completion.
    It retrieves the order details and returns them in the response.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """
        Handles GET requests to retrieve order details after successful payment.
        """
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
