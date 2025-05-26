from django.urls import path
from django.contrib.auth.views import LogoutView

from .views.accounts import views
from .views.profile import views as profile_views

app_name = "accounts"

urlpatterns = [
    path("email_check_sign_up/", views.email_check_sign_up, name="email_check_sign_up"),
    path("sign_up/", views.signup_view, name="sign_up"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="shop:product_list"), name="logout"),
    path("profile/", profile_views.profile_view, name="profile"),
    path("profile/edit/", profile_views.edit_profile_view, name="profile_edit"),
]
