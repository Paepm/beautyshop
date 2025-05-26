from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from devtools import debug

from .models import Item
from .services.shop_service import ShopService


def product_list(request):
    """
    Display the list of available products in the shop.
    """
    products = Item.objects.all()
    return render(request, 'shop/product_list.html', {"products": products})

def about(request):
    """
    Render the 'About Us' page.
    """
    return render(request, 'shop/about.html')

def contact(request):
    """
    Render the contact page with contact information.
    """
    return render(request, 'shop/contact.html')

def privacy(request):
    """
    Render the privacy (imprint) page.
    """
    return render(request, 'shop/privacy.html')

def agb(request):
    """
    Render the AGB (terms of service) page.
    """
    return render(request, 'shop/agb.html')

def terms_and_conditions(request):
    """
    Render the terms and conditions page.
    """
    return render(request, 'shop/terms_and_conditions.html')

@login_required
def add_to_cart(request, product_id):
    """
    Add the selected product to the user's cart.
    If the product is already in the cart, increment the quantity.

    Args:
        request (HttpRequest): The request object containing user and session info.
        product_id (int): The ID of the product to add.

    Returns:
        HttpResponseRedirect: Redirects to the referring page or the product list.
    """
    ShopService(request.user).add_to_cart(product_id)
    return redirect(request.META.get('HTTP_REFERER') or reverse('shop:product_list'))
