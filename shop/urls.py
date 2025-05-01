from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('agb/', views.agb, name='agb'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('signup/', views.signup_view, name='signup'),
    path('cart/add/<int:product_id>/', views.add_to_card, name='add_to_cart'),

]