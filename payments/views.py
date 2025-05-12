from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from devtools import debug

from orders.services.order_creator import OrderCreator
from cart.services.cart_services import CartService
from payments.services.payment_service import PaymentService

@login_required
def select_payment_method_view(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        payment_service = PaymentService(request.user)

        # 1. paymethod validation
        if not payment_service.validate_pay_method(method):
            return render(request, 'select_payment_method.html', {
                'error': 'Invalid payment method selected.'
            })

        # 2. paymethod remember in session
        request.session['selected_payment_method'] = method
        debug("SELECTED PAYMENT METHOD:", method)
        debug(request.session)


        # 3. Redirect to final order creation
        return redirect('orders:create_order_after_payment')

    # GET: show page
    return render(request, 'select_payment_method.html')
