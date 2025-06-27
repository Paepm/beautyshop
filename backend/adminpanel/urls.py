from django.urls import path

from adminpanel.views.admin_order_view import (
    AdminOrderListView,
    AdminOrderDetailView,
    AdminOrderExportView,
)
from adminpanel.views.admin_user_view import AdminUserListView
from adminpanel.views.admin_order_status_handler import AdminOrderStatusHandlerView
from adminpanel.views.admin_stock_updater_view import AdminStockUpdaterView

app_name = "adminpanel"

urlpatterns = [
    path("orders/", AdminOrderListView.as_view(), name="admin_order_list"),
    path("orders/export/", AdminOrderExportView.as_view(), name="admin-orders-export"),
    path("orders/<int:pk>/", AdminOrderDetailView.as_view(), name="admin_order_detail"),
    path("users/", AdminUserListView.as_view(), name="admin_user_list"),
    path(
        "orders_status_manager/<int:pk>/",
        AdminOrderStatusHandlerView.as_view(),
        name="admin_order_status_handler",
    ),
    path("stock_updater/", AdminStockUpdaterView.as_view(), name="admin_stock_updater"),
]
