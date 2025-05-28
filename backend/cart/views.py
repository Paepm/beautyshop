from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from devtools import debug
from django.http import JsonResponse

from .services.cart_services import CartService


@login_required
def cart_detail_api(request):
    """
    Return the cart items and total price as JSON.
    Used by the React frontend.
    """
    service: CartService = CartService(request.user)
    cart_items: list = service.get_cart_items()

    items_data = [
        {
            "id": item.id,
            "quantity": item.quantity,
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "price": float(item.product.price),
                "image": item.product.image.url if item.product.image else None,
            },
        }
        for item in cart_items
    ]

    return JsonResponse(
        {
            "items": items_data,
            "total_price": float(service.get_total_price()),
        }
    )


@require_POST
@login_required
def add_product_to_cart(request, item_id):
    """
    Update the quantity of a specific item in the cart.
    Expects a POST request with 'action' or 'quantity' in the body.
    """
    action = request.POST.get("action")
    quantity = request.POST.get("quantity")

    CartService(request.user).update_quantity(
        item_id=item_id, action=action, quantity=quantity
    )

    if not action and not quantity:
        return JsonResponse(
            {"success": False, "error": "No update parameters provided"}, status=400
        )

    return JsonResponse({"success": True})
