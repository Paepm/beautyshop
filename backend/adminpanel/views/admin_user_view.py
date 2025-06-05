from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from devtools import debug

from adminpanel.service.permissions import IsSuperUser
from adminpanel.service.admin_user_service import AdminUserService


class AdminUserListView(APIView):
    """
    API View that returns all orders for admin users.
    """

    permission_classes = [IsSuperUser]

    def get(self, request):

        serializer = AdminUserService().get_all_users()
        debug("serializer: ", serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
