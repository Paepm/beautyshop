from django.urls import path

from .views.accounts.api_info import AuthInfoView
from .views.accounts import views as account_views
from .views.accounts.api_auth import logout_view


# This api_urls.py is for the React frontend
app_name = "accounts"


urlpatterns = [
    path("login/", account_views.login_view, name="login"),
    path("sign_up/", account_views.signup_view, name="sign_up"),
    path("logout/", logout_view, name="logout"),
    path("me/", AuthInfoView.as_view(), name="auth_info"),
    path("api/get-csrf/", AuthInfoView.as_view, name="get_csrf_token"),
]
