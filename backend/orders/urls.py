from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('finalize/', views.create_order_after_payment_view, name='create_order_after_payment'),
    path('success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('my-orders/', views.user_order_list_view, name='user_order_list'),
    path('my-orders/<int:order_id>/', views.user_order_detail_view, name='user_order_detail'),
    path('review/', views.user_order_review_view, name='order_review'),
]