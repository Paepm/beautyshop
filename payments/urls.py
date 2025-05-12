from django.urls import path

from payments import views


app_name = 'payments'

urlpatterns = [
    path('create/', views.select_payment_method_view, name='create_payment'),
    # path('success/<int:order_id>/', views.payment_success_view, name='payment_success'),
    # path('cancel/<int:payment_id>/', views.payment_cancel_view, name='payment_cancel'),
]