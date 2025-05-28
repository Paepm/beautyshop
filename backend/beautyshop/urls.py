from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from beautyshop.settings import BASE_DIR
from django.contrib.auth import views as auth_views
from django.contrib import admin

import os

urlpatterns = [
    path("admin/", admin.site.urls),
    # paths for django password resetter --> is global needed that it works....
    path(
        "emails/password_reset_confirm/<str:uidb64>/<str:token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "emails/password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "emails/password_reset_complete/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_complete",
    ),
    # Urls for FRONTEND STUFF TO GET PRODUCTS AS JSON
    path("api/products/", include("shop.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/emails/", include("emails.urls", namespace="emails")),
    path("api/cart/", include("cart.urls")),
]

# for the template static files
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=os.path.join(BASE_DIR, "static")
    )

# for the media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
