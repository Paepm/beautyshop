from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from backend.cart.services.cart_services import CartService


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service: CartService = CartService(request.user)
        cart_products: list = service.get_cart_products()
        total_price = service.get_total_price()

        return Response(
            {
                "items": [
                    {
                        "id": product.id,
                        "quantity": product.quantity,
                        "product": {
                            "id": product.product.id,
                            "name": product.product.name,
                            "price": float(product.product.price),
                            "image": (
                                product.product.image.url
                                if product.product.image
                                else None
                            ),
                        },
                    }
                    for product in cart_products
                ],
                "total_price": float(total_price),
            }
        )


class CartAddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        service = CartService(request.user)
        item = service.add_product(product_id=product_id)

        if item:
            return Response({"success": True})

        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


class CartUpdateQuantityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        action = request.data.get("action")
        quantity = request.data.get("quantity")

        if not action and not quantity:
            return Response(
                {"success": False, "error": "No update data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = CartService(request.user)
        success = service.update_quantity(
            product_id=product_id, action=action, quantity=quantity
        )

        if success:
            return Response({"success": True})

        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


class CartRemoveProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        service = CartService(request.user)
        success = service.remove_product(product_id=product_id)

        if success:
            return Response({"success": True})

        return Response(
            {"success": False, "error": "product not found in cart"},
            status=status.HTTP_404_NOT_FOUND,
        )
