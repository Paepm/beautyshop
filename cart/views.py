from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    })
