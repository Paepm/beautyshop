from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from devtools import debug
from django.urls import reverse

from payments.services.payment_service import PaymentService
from payments.services.payment_service import PaymentService
from orders.services.order_service import OrderService


@login_required
def select_payment_provider_view(request):
    """
    Displays the payment provider selection page and processes user input.

    On GET requests, renders a template with the list of supported payment providers.
    On POST requests, validates the selected provider and stores it in the session.
    If the provider is valid, redirects to the payment start view.
    If invalid, re-renders the form with an error message.

    Args:
        request (HttpRequest): The HTTP request object containing session and POST data.

    Returns:
        HttpResponse: Rendered template or redirect to the next step in the payment flow.
    """
    payment_service = PaymentService(request.user)
    supported_providers: list = payment_service.get_supported_payment_providers()

    # check if the form was submitted and checked if its no GHOSTPOST (first time entering page, had the wrong payment error..)
    if request.method == "POST" and "submit_btn" in request.POST:
        # debug("POST DATA:", request.POST)
        provider = request.POST.get("provider")
        # debug("METHOD:", method)

        # 1. validate provider
        if not payment_service.validate_payment_provider(provider):
            return render(
                request,
                "select_payment_provider.html",
                {
                    "supported_providers": supported_providers,
                    "error": "Invalid payment provider selected.",
                },
            )

        # 2. valid input --> next step --> save in session
        request.session["selected_payment_provider"] = provider
        # debug("SELECTED PAYMENT METHOD:", method)
        # debug("SESSION AFTER SELECTION:", dict(request.session))

        # 3. conditional redirect based on method
        return redirect("payments:start_payment")

    # GET: show page
    return render(
        request,
        "select_payment_provider.html",
        {"supported_providers": supported_providers},
    )


@login_required
def start_payment_view(request):
    """
    Initiates the payment process using the selected payment method.

    Retrieves the selected payment method from the session, validates it,
    creates or retrieves an order, and redirects the user to the external
    Stripe Checkout page. If any validation fails, the user is redirected
    back to the payment method selection or error page.

    After initiating the checkout, the selected payment method is removed
    from the session to allow clean state for future purchases.

    Args:
        request (HttpRequest): The HTTP request object from the user.

    Returns:
        HttpResponseRedirect: Redirect to Stripe Checkout or another view
        depending on success, failure, or missing data.
    """
    provider = request.session.get("selected_payment_provider")

    if not provider:
        return redirect("payments:select_payment_provider")

    payment_service = PaymentService(request.user)

    # Validate
    if not payment_service.validate_payment_provider(provider):
        return redirect("payments:select_payment_provider")

    # create order
    order_service = OrderService(user=request.user, request=request)
    order = order_service.process_order(payment_provider=provider)

    if not order:
        request.session["error_message"] = "Could not create order."
        return redirect("payments:error_payment")

    success_url = request.build_absolute_uri(
        reverse("orders:order_success", args=[order.id])
    )
    cancel_url = request.build_absolute_uri(reverse("payments:cancel_payment"))

    # Stripe Checkout start
    response = payment_service.process_payment(
        provider_key=provider,
        order=order,
        success_url=success_url,
        cancel_url=cancel_url,
    )

    if response.get("status") == "unsupported":
        return render(request, "error.html", {"error": response.get("message")})

    # delete the selected payment method from session that in new session the user can select a new payment method
    request.session.pop("selected_payment_provider", None)

    return redirect(
        response["redirect_url"]
    )  # <--- here we redirect to the Stripe Checkout URL


@login_required
def cancel_payment_view(request):
    """
    Handles user-initiated cancellation from Stripe Checkout.
    Marks the current order as failed
    """
    order_service = OrderService(user=request.user, request=request)
    order = order_service.get_existing_open_order()

    if order:
        order_service = OrderService(request.user, request, order)
        order_service.set_payment_cancelled()

    request.session["error_message"] = "Payment was cancelled."
    return redirect("payments:error_payment")


@login_required
def error_payment_view(request):
    error = request.session.pop("error_message", "an unknown error occurred")
    return render(request, "error.html", {"error": error})
