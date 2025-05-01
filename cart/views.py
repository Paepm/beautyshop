from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from devtools import debug

from .models import Cart, CartItem

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.get_total_price() for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'login_required': request.user.is_authenticated,
    })

@login_required
def remove_product_from_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            item = get_object_or_404(CartItem, id=product_id, cart=cart)
            item.delete()
        except Cart.DoesNotExist:
            pass

        return redirect('cart:cart_detail')

    return HttpResponseNotAllowed(['POST'])

@login_required
@require_POST
def update_cart_item_quantity(request, item_id):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    action = request.POST.get("action")
    quantity = request.POST.get("quantity")

    if action == "increment":
        item.quantity += 1
    elif action == "decrement":
        item.quantity = max(1, item.quantity - 1) # Ensure quantity doesn't go below 1
    elif quantity:
        try:
            quantity = int(quantity)
            item.quantity = max(1, quantity) # Ensure quantity doesn't go below 1
        except ValueError:
            pass # Handle invalid quantity input
            
    item.save()
    return redirect('cart:cart_detail')
            

