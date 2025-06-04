from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.services.pw_reset_service import PwResetService


class RequestPwResetView(APIView):

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"status": "error", "message": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = PwResetService()
        success, message = service.send_password_reset_link(email)

        return Response(
            {"status": "success" if success else "error", "message": message}
        )


class ResetPwWithTokenView(APIView):

    def post(self, request, token: str):
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"status": "error", "message": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = PwResetService()
        success, message = service.reset_password_with_token(token, new_password)

        return Response(
            {"status": "success" if success else "error", "message": message},
            status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST,
        )
