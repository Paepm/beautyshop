from django.urls import path
from . import views

# This api_urls.py is for the React frontend

urlpatterns = [
    path("", views.api_product_list, name="api_product_list"),
]
