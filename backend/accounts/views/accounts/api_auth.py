from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from devtools import debug

from backend.accounts.services.login_service import LoginService


@api_view(["POST"])
@ensure_csrf_cookie
def api_login_view(request):
    username_or_email = request.data.get("username_or_email")
    password = request.data.get("password")

    if not username_or_email or not password:
        return Response(
            {"error": "Missing credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    login_service = LoginService(request, username_or_email, password)

    if login_service.authenticate_user():
        login_service.login_user()
        user = login_service.get_user()
        debug("[API_LOGIN_VIEW]User authenticated and logged in: ", user)
        return Response(
            {"message": "Login successful", "user": user.username},
            status=status.HTTP_200_OK,
        )
    else:
        debug("[API_LOGIN_VIEW]Invalid credentials for user: ", username_or_email)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@csrf_protect
@api_view(["POST"])
def logout_view(request):
    """
    Logs out the user by clearing the session.
    Returns a 204 No Content response.
    """
    debug("[LOGOUT_VIEW]BEFORE logout: user = ", request.user)
    logout(request)
    request.session.flush()
    debug("[LOGOUT_VIEW]AFTER logout and flush: user = ", request.user)
    return JsonResponse({"message": "Logged out"}, status=204)
