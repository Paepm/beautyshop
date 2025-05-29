from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("", views.cart_detail_api, name="cart_detail"),
    path(
        "add/<int:product_id>/", views.add_product_to_cart, name="add_product_to_cart"
    ),
    path(
        "update/<int:product_id>/", views.update_cart_product, name="update_cart_item"
    ),
    path(
        "remove/<int:product_id>/",
        views.remove_cart_product,
        name="remove_cart_product",
    ),
]
