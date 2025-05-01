from django.shortcuts import render
from .models import Product, Category

# Create your views here.

def product_list(request):
    # Logic to retrieve and display products
    products = Product.objects.all()
    return render(request, 'shop/index.html', {"products": products})

