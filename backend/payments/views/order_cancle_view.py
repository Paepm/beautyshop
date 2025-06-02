from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class OrderCancleView(APIView):
    """
    Order cancellation view.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle order cancellation requests.
        """
        # Logic for handling order cancellation
        return Response({"message": "Order cancelled successfully."}, status=200)
