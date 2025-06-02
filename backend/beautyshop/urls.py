from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from beautyshop.settings import BASE_DIR
from django.contrib.auth import views as auth_views
from django.contrib import admin

import os

urlpatterns = [
    path("admin/", admin.site.urls),
    # Urls for FRONTEND STUFF TO GET PRODUCTS AS JSON
    path("api/products/", include("shop.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("api/orders/", include(("orders.urls", "orders"), namespace="orders")),
    path("api/payments/", include(("payments.urls", "payments"), namespace="payments")),
]

# for the media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
