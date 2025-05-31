from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import AnonymousUser
from devtools import debug


@method_decorator(ensure_csrf_cookie, name="dispatch")
class AuthInfoView(View):
    def get(self, request):
        user = request.user
        debug("[AuthInfoView] GET request received. User: ", user)
        debug("Cookies:", request.COOKIES)

        if isinstance(user, AnonymousUser) or not user.is_authenticated:
            debug("[AuthInfoView] User is not authenticated -->", user.is_authenticated)
            return JsonResponse(
                {"detail": "Authentication required."}, status=401  # <- important!
            )
        debug("[AuthInfoView] User is authenticated: ", user)
        return JsonResponse(
            {
                "is_authenticated": True,
                "username": user.username,
                "email": user.email,
            }
        )
