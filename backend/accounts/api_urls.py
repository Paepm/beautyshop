from django.urls import path
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .views.accounts import csrf
from .views.accounts import views as account_views


# This api_urls.py is for the React frontend
app_name = "accounts"


@csrf_exempt
@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=204)


urlpatterns = [
    path("get-csrf/", csrf.get_csrf_token, name="get_csrf_token"),
    path("login/", account_views.login_view, name="login"),
    path("sign_up/", account_views.signup_view, name="sign_up"),
    path("logout/", logout_view, name="logout"),
]
