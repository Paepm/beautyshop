from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(ensure_csrf_cookie, name="dispatch")
class AuthInfoView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse(
                {
                    "is_authenticated": True,
                    "username": request.user.username,
                    "email": request.user.email,
                }
            )
        else:
            return JsonResponse({"is_authenticated": False})
