from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('update/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item'),


]