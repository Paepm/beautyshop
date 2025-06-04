from django.urls import path

from .views.api_info_view import AuthInfoView
from .views.login_logout_view import LoginAPIView, LogoutAPIView
from .views.user_profile_view import CountryListView, ProfileView
from .views.reset_pw_view import RequestPwResetView, ResetPwWithTokenView
from .views.signup_view import SignupAPIView, VerifyAccountAPIView


# This api_urls.py is for the React frontend
app_name = "accounts"


urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("sign_up/", SignupAPIView.as_view(), name="sign_up"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("get-csrf/", AuthInfoView.as_view(), name="get_csrf_token"),
    path("countries/", CountryListView.as_view(), name="country_list"),
    path("verify/<str:token>/", VerifyAccountAPIView.as_view(), name="verify_email"),
    path("password_reset/", RequestPwResetView.as_view(), name="password_forgot_reset"),
    path(
        "password_reset/<str:token>/",
        ResetPwWithTokenView.as_view(),
        name="password_reset_token",
    ),
]
