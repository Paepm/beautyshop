from django.urls import path
from .views.api_views import (
    CartAddProductView,
    CartDetailView,
    CartUpdateQuantityView,
    CartRemoveProductView,
)


app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart_detail"),
    path(
        "add/<int:product_id>/",
        CartAddProductView.as_view(),
        name="add_product_to_cart",
    ),
    path(
        "update/<int:product_id>/",
        CartUpdateQuantityView.as_view(),
        name="update_cart_item",
    ),
    path(
        "remove/<int:product_id>/",
        CartRemoveProductView.as_view(),
        name="remove_cart_product",
    ),
]
