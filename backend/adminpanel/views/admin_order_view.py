from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from adminpanel.service.permissions import IsSuperUser
from adminpanel.service.admin_order_service import AdminOrderService


class AdminOrderListView(APIView):
    """
    API View that returns all orders for admin users.
    """

    permission_classes = [IsSuperUser]

    def get(self, request):

        serializer = AdminOrderService().get_all_orders()

        return Response(serializer.data, status=status.HTTP_200_OK)
