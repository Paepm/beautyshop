from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from devtools import debug

from orders.services.order_creator import OrderCreator
from cart.services.cart_services import CartService
from payments.services.payment_service import PaymentService
from orders.models import Order

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
        return redirect('payments:start_stripe_payment')

    # GET: show page
    return render(request, 'select_payment_method.html')

@login_required
def start_stripe_payment_view(request):
    method = request.session.get("selected_payment_method")
    if not method:
        return redirect("payments:select_payment_method")

    payment_service = PaymentService(request.user)

    if not payment_service.validate_pay_method(method):
        return redirect("payments:select_payment_method")

    # Beispielwert, z. B. aus CartService berechnet
    amount = CartService(request.user).get_total_price()

    # Dummy Stripe Payment starten
    response = payment_service.process_payment(order=None, amount=amount, method=method)
    debug(response)

    # ✅ NEU: Button zur „Order erstellen“-View mit finalem Redirect
    return render(request, "payments/stripe_start.html", {
        "response": response
    })

