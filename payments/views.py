from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from devtools import debug

from orders.services.order_service import OrderCreator
from cart.services.cart_services import CartService


@login_required
def select_payment_method_view(request):
    if request.method == 'POST':
        # formular sended
        method = request.POST.get('method')

        if method not in ['card', 'paypal', 'invoice', 'bank_transfer', 'crypto', 'klara']:
            return render(request, 'select_payment_method.html', {
                'error': 'Invalid payment method selected.'
            })
        
        request.session['selected_payment_method'] = method

        order = OrderCreator(user=request.user).create_order()
        order.payment_method = method
        order.save()
        request.session['order_id'] = order.id
        debug("ORDER ID:", order.id)

        CartService(request.user).clear_cart()
        
        return redirect('orders:order_success', order_id=order.id)  

    return render(request, 'select_payment_method.html')
