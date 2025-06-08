from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from devtools import debug

from accounts.services.login_service import LoginService


class LoginAPIView(APIView):

    def post(self, request):
        # get data from react user input
        username_or_email = request.data.get("username_or_email")
        password = request.data.get("password")
        debug(username_or_email, "adad", password)

        if not username_or_email or not password:
            return Response(
                {
                    "status": "error",
                    "message": "Username or email and password are required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = LoginService(request, username_or_email, password)
        if service.authenticate_user():
            service.login_user()
            user = service.get_user()
            return Response(
                {"message": "Login successful", "user": user.username},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)
        request.session.flush()  # Clear the session data
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_204_NO_CONTENT,
        )
