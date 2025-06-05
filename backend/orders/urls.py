from django.urls import path

from .views.orders_view import OrderListView, OrderDetailView, OrderProductDetailView


app_name = "orders"

urlpatterns = [
    path("orderlist/", OrderListView.as_view(), name="order_list"),
    path(
        "order_detail/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"
    ),
    path(
        "order_product/<int:order_id>/",
        OrderProductDetailView.as_view(),
        name="order_product_detail",
    ),
]
