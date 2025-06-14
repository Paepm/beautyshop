from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from wishlist.serializer.serializer import WishlistItemSerializer
from wishlist.services.wishlist_service import WishlistService


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = WishlistService.list_items(request.user)
        serializer = WishlistItemSerializer(items, many=True)
        return Response(serializer.data)

    def delete(self, request):
        WishlistService.clear_wishlist(request.user)
        return Response(
            {"message": "Wishlist cleared."}, status=status.HTTP_204_NO_CONTENT
        )


class WishlistAddRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        item = WishlistService.add_product(request.user, product_id)
        serializer = WishlistItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        WishlistService.remove_product(request.user, product_id)
        return Response(
            {"message": "Product removed."}, status=status.HTTP_204_NO_CONTENT
        )
