from django.urls import path

from .views.accounts.api_info import AuthInfoView
from .views.accounts.api_auth import logout_view, api_login_view
from .views.accounts.profile import user_profile_view, CountryListView
from .views.accounts.signup import SignupAPIView


# This api_urls.py is for the React frontend
app_name = "accounts"


urlpatterns = [
    path("login/", api_login_view, name="login"),
    path("sign_up/", SignupAPIView.as_view(), name="sign_up"),
    path("profile/", user_profile_view, name="profile"),
    path("logout/", logout_view, name="logout"),
    path("me/", AuthInfoView.as_view(), name="auth_info"),
    path("get-csrf/", AuthInfoView.as_view(), name="get_csrf_token"),
    path("countries/", CountryListView.as_view(), name="country_list"),
]
