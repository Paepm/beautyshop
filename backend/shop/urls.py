from django.urls import path
from .views import ProductListView, ProductDetailView

# This api_urls.py is for the React frontend

urlpatterns = [
    path("", ProductListView.as_view(), name="api_product_list"),
    path("<int:product_id>/", ProductDetailView.as_view(), name="api_product_detail"),
]
