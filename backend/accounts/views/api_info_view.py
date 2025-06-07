from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from devtools import debug


@method_decorator(ensure_csrf_cookie, name="dispatch")
class AuthInfoView(APIView):
    """
    Returns authentication status and user info.
    Also sets CSRF cookie for the frontend on first GET.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # debug("[AuthInfoView] GET request received. User: ", user)
        # debug("Cookies:", request.COOKIES)

        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            debug("[AuthInfoView] User is not authenticated -->", user.is_authenticated)
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        debug("[AuthInfoView] User is authenticated: ", user)
        return Response(
            {
                "is_authenticated": True,
                "username": user.username,
                "email": user.email,
                "is_superuser": request.user.is_superuser,
            },
            status=status.HTTP_200_OK,
        )
