from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from orders.services.order_service import OrderCreator
from cart.services.cart_services import CartService
from .models import Order


@login_required
def create_order_view(request):
    if request.method == 'POST':
        service = OrderCreator(user=request.user)
        order = service.create_order()

        return redirect('orders:order_success', order_id=order.id)
    
    return redirect('cart:cart_detail')


def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart_service = CartService(user=request.user)
    cart_service.clear_cart()  # Clear the cart after order successed
    return render(request, 'order_success.html', {'order': order})


def user_order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_order_list.html', {'orders': orders})

def user_order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'user_order_detail.html', {'order': order})

def user_order_review_view(request):
    cart_service = CartService(user=request.user)
    cart_items = cart_service.get_cart_items()
    total_price = cart_service.get_total_price()
    return render(request, 'order_review.html', {"cart_items": cart_items, "total_price": total_price})
