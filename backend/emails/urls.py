from django.urls import path
from django.contrib.auth import views as auth_views

from emails.views import views
from emails.views.password_reset_views import CustomPasswordResetConfirmView

app_name = "emails"

urlpatterns = [
    path("verify/<str:token>/", views.verify_account_view, name="verify_email"),
    path(
        "password_reset_email/",
        auth_views.PasswordResetView.as_view(
            template_name="emails/password_reset.html"
        ),
        name="password_reset_email",
    ),
    path(
        "password_reset_confirm/<str:uidb64>/<str:token>/",
        CustomPasswordResetConfirmView.as_view(
            template_name="emails/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="emails/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="emails/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<str:uidb64>/<str:token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
