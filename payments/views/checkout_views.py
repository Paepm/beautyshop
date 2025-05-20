from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from devtools import debug
from django.urls import reverse

from payments.services.payment_service import PaymentService
from payments.services.payment_service import PaymentService
from orders.services.order_service import OrderService


@login_required
def select_payment_method_view(request):
    payment_service = PaymentService(request.user)
    supported_methods = payment_service.get_supported_methods()

    # check if the form was submitted and checked if its no GHOSTPOST (first time entering page, had the wrong payment error..)
    if request.method == "POST" and "submit_btn" in request.POST:
        # debug("POST DATA:", request.POST)
        method = request.POST.get("method")
        # debug("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa", method)

        # 1. validate method
        if not payment_service.validate_pay_method(method):
            return render(
                request,
                "select_payment_method.html",
                {
                    "supported_methods": supported_methods,
                    "error": "Invalid payment method selected.",
                },
            )

        # 2. valid input --> next step --> save in session
        request.session["selected_payment_method"] = method
        # debug("SELECTED PAYMENT METHOD:", method)
        # debug("SESSION AFTER SELECTION:", dict(request.session))

        # 3. conditional redirect based on method
        return redirect("payments:start_payment")

    # GET: show page
    return render(
        request, "select_payment_method.html", {"supported_methods": supported_methods}
    )


@login_required
def start_payment_view(request):
    method = request.session.get("selected_payment_method")
    if not method:
        return redirect("payments:select_payment_method")

    payment_service = PaymentService(request.user)

    # Validate
    if not payment_service.validate_pay_method(method):
        return redirect("payments:select_payment_method")

    # Order erstellen
    order_service = OrderService(user=request.user, request=request)
    order = order_service.process_order(payment_method=method)

    if not order:
        request.session["error_message"] = "Could not create order."
        return redirect("payments:error")

    # Stripe Checkout starten (oder anderer Provider)
    response = payment_service.process_payment(
        amount=order.total_price,
        method=method,
        order=order,
        success_url=request.build_absolute_uri(
            reverse("orders:order_success", args=[order.id])
        ),
        cancel_url=request.build_absolute_uri(
            reverse("payments:select_payment_method")
        ),
    )

    if response.get("status") == "unsupported":
        return render(request, "error.html", {"error": response.get("message")})

    return redirect(
        response["redirect_url"]
    )  # <--- Hier leiten wir direkt zu Stripe um


@login_required
def error_payment_view(request):
    error = request.session.pop("error_message", "an unknown error occurred")
    return render(request, "error.html", {"error": error})
