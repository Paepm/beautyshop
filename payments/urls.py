from django.urls import path

from payments import views


app_name = 'payments'

urlpatterns = [
    path('create/', views.select_payment_method_view, name='create_payment'),
    path('stripe/', views.start_payment_view, name='start_payment'),
    path('error/', views.error_payment_view, name='error_payment'),
]