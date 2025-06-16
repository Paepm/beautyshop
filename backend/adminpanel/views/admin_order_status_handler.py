from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from devtools import debug
from adminpanel.service.permissions import IsSuperUser

from adminpanel.service.admin_order_service import AdminOrderService
from orders.models import Order


class AdminOrderStatusHandlerView(APIView):
    """
    Handles the admin status endpoint.
    """

    permission_classes = [IsSuperUser]

    def patch(self, request, pk: int):

        # get the status from frontend
        new_order_status: str = request.data.get("order_status")
        new_shipping_provider: str = request.data.get("shipping_provider")
        new_tracking_id: str = request.data.get("tracking_id")
        new_tracking_url: str = request.data.get("tracking_url")

        update_data = AdminOrderService().update_order_and_tracking_status(
            pk,
            new_order_status,
            new_shipping_provider,
            new_tracking_id,
            new_tracking_url,
        )
        debug("UPDATE DATA", update_data)

        return Response(
            {
                "message": "Order updated successfully.",
                "order": update_data,
            },
            status=status.HTTP_200_OK,
        )
