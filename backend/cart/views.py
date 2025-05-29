from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from devtools import debug
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from backend.shop.services.shop_service import ShopService
from .services.cart_services import CartService


@ensure_csrf_cookie
def csrf_cookie_view(request):
    return JsonResponse({"message": "CSRF cookie set"})


@login_required
def cart_detail_api(request):
    """
    Return the cart items and total price as JSON.
    Used by the React frontend.
    """
    service: CartService = CartService(request.user)
    cart_products: list = service.get_cart_products()

    products_data = [
        {
            "id": product.id,
            "quantity": product.quantity,
            "product": {
                "id": product.product.id,
                "name": product.product.name,
                "price": float(product.product.price),
                "image": product.product.image.url if product.product.image else None,
            },
        }
        for product in cart_products
    ]

    return JsonResponse(
        {
            "items": products_data,
            "total_price": float(service.get_total_price()),
        }
    )


@require_POST
@login_required
def add_product_to_cart(request, product_id):

    action = request.POST.get("action")

    if not action:
        debug("[ADD_PRODUCT_TO_CART] No action or quantity provided")
        return JsonResponse(
            {"success": False, "error": "No update parameters provided"}, status=400
        )

    shop_service = ShopService(request.user)
    shop_service.add_to_cart(product_id=product_id)

    return JsonResponse({"success": True})


@require_POST
@login_required
def update_cart_item(request, product_id):
    action = request.POST.get("action")
    quantity = request.POST.get("quantity")

    print("UPDATE ITEM: action:", action)
    print("UPDATE ITEM: quantity:", quantity)

    if not action and not quantity:
        return JsonResponse(
            {"success": False, "error": "Keine Aktion angegeben"}, status=400
        )

    CartService(request.user).update_quantity(
        item_id=product_id, action=action, quantity=quantity
    )

    return JsonResponse({"success": True})
