from django.urls import path

from . import views_django
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
    # path(
    #     "finalize/",
    #     views_django.create_order_after_payment_view,
    #     name="create_order_after_payment",
    # ),
    # path(
    #     "success/<int:order_id>/", views_django.order_success_view, name="order_success"
    # ),
    # path("my-orders/", views_django.user_order_list_view, name="user_order_list"),
    # path(
    #     "my-orders/<int:order_id>/",
    #     views_django.user_order_detail_view,
    #     name="user_order_detail",
    # ),
    # path("review/", views_django.user_order_review_view, name="order_review"),
]
