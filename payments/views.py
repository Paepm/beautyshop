from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from devtools import debug
from django.conf import settings

from cart.services.cart_services import CartService
from payments.services.payment_service import PaymentService
from orders.models import Order
from payments.services.payment_service import PaymentService


@login_required
def select_payment_method_view(request):
    payment_service = PaymentService(request.user)
    supported_methods = payment_service.get_supported_methods()

    # check if the form was submitted and checked if its no GHOSTPOST (first time entering page, had the wrong payment error..)
    if request.method == 'POST' and 'submit_btn' in request.POST: 
        # debug("POST DATA:", request.POST)
        method = request.POST.get('method')
        # debug("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa", method)
        
        # 1. validate method
        if not payment_service.validate_pay_method(method):
            return render(request, 'select_payment_method.html', {
                'supported_methods': supported_methods,
                'error': "Invalid payment method selected."
            })

        # 2. valid input --> next step --> save in session
        request.session['selected_payment_method'] = method
        # debug("SELECTED PAYMENT METHOD:", method)
        # debug("SESSION AFTER SELECTION:", dict(request.session))

        # 3. conditional redirect based on method
        return redirect("payments:start_payment")

    # GET: show page
    return render(request, 'select_payment_method.html', {
        'supported_methods': supported_methods
    })


@login_required
def start_payment_view(request):

    #debug("START STRIPE – Session:", dict(request.session))
    method = request.session.get("selected_payment_method") # get selected payment method from session
    # debug("SELECTED PAYMENT METHOD:", method)

    # prevents manipulation or wrong payment method
    if not method:
        return redirect("payments:select_payment_method")

    payment_service = PaymentService(request.user)
    if not payment_service.validate_pay_method(method):
        return redirect("payments:select_payment_method")

    # calculate total price of the cart
    amount = CartService(request.user).get_total_price()
    # debug("TOTAL PRICE:", amount)

    # Stripe Payment start
    response = payment_service.process_payment(amount=amount, method=method)
    # debug(response)

    if response.get("status") == 'unsupported':
        return render(request, 'error.html', {
            'error': response.get("message")
        })

    # go to payment page
    return render(request, "stripe_start.html", {
        "client_secret": response["client_secret"],
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })

@login_required
def error_payment_view(request):
    error = request.session.pop('error_message', 'an unknown error occurred')
    return render(request, 'error.html', {'error': error})


