from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from devtools import debug

from .models import Item
from cart.models import Cart
from cart.models import CartItem


# Create your views here.

def product_list(request):
    # Logic to retrieve and display products
    products = Item.objects.all()
    # debug(products)
    return render(request, 'shop/product_list.html', {"products": products})

def about(request):
    # Logic to display the about page
    return render(request, 'shop/about.html')

def contact(request):
    # Logic to display the contact page
    return render(request, 'shop/contact.html')

def privacy(request):
    # Logic to display the imprint page
    return render(request, 'shop/privacy.html')

def agb(request):
    # Logic to display the terms and conditions page
    return render(request, 'shop/agb.html')

def terms_and_conditions(request):
    # Logic to display the terms and conditions page
    return render(request, 'shop/terms_and_conditions.html')



@login_required
def add_to_card(request, product_id):
    product = get_object_or_404(Item, id=product_id)

    # get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # if the product is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # add product to cart and stay on same page
    print("REFERER:", request.META.get('HTTP_REFERER', ''))
    return redirect(request.META.get('HTTP_REFERER')) or reverse('shop:product_list')

