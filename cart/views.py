from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from devtools import debug

from .services.cart_services import CartService

@login_required
def cart_detail(request):
    """"Display the cart detail page."""
    service = CartService(request.user)
    debug(service.get_total_price())
    return render(request, 'cart/cart_detail.html', {
        'cart_items': service.get_cart_items(),
        'total_price': service.get_total_price(),
        'login_required': request.user.is_authenticated,
    })


@login_required
@require_POST
def remove_product_from_cart(request, product_id):
    """Remove a product from the cart and redirect to the cart detail page."""      
    CartService(request.user).remove_item(product_id)

    return redirect('cart:cart_detail')

@login_required
@require_POST
def update_cart_item_quantity(request, item_id):
    """update the quantity of a cart item and redirect to the cart detail page."""
    action = request.POST.get('action')
    quantity = request.POST.get('quantity')
    CartService(request.user).update_quantity(item_id=item_id, action=action, quantity=quantity)
    return redirect('cart:cart_detail')
            

