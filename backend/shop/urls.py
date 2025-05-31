from django.urls import path
from . import views

# This api_urls.py is for the React frontend

urlpatterns = [
    path("", views.product_list, name="api_product_list"),
    path("<int:pk>/", views.product_detail_view, name="api_product_detail"),
]
