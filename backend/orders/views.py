from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from devtools import debug

from orders.services.order_service import OrderCreator
from cart.services.cart_services import CartService
from .models import Order
from payments.services.payment_service import PaymentService
from beautyshop.logging_config import setup_logger
from payments.services.providers.stripe_provider import StripeProvider
from payments.enums.payment_providers import PaymentProviders

# create a logger instance
logger = setup_logger(__name__)


@login_required
def create_order_after_payment_view(request):
    method = request.session.get("selected_payment_method")
    order_id = request.session.get("order_id")

    if not method or not order_id:
        logger.warning(
            f"[ORDER] No payment method or order_id in session for user: {request.user.email}"
        )
        return redirect("cart:cart_detail")

    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        logger.error(f"[ORDER] No matching order found with ID {order_id}")
        return redirect("cart:cart_detail")

    payment_service = PaymentService(request.user)

    if not payment_service.validate_payment_provider(method):
        logger.warning(
            f"[ORDER] Invalid payment method selected for user: {request.user.email}"
        )
        return redirect("cart:cart_detail")

    payment_service.save_payment_provider_to_order(order, method)

    CartService(request.user).clear_cart()

    request.session.pop("selected_payment_method", None)
    request.session.pop("order_id", None)

    return redirect("orders:order_success", order_id=order.id)


def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart_service = CartService(user=request.user)
    cart_service.clear_cart()  # Clear the cart after order successed
    return render(request, "order_success.html", {"order": order})


def user_order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(
        request,
        "user_order_list.html",
        {
            "orders": orders,
        },
    )


def user_order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "user_order_detail.html", {"order": order})


def user_order_review_view(request):
    cart_service = CartService(user=request.user)
    cart_items = cart_service.get_cart_items()
    total_price = cart_service.get_total_price()
    return render(
        request,
        "order_review.html",
        {"cart_items": cart_items, "total_price": total_price},
    )
