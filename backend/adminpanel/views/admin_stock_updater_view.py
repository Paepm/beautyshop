from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from devtools import debug

from adminpanel.service.permissions import IsSuperUser
from adminpanel.service.admin_product_service import AdminProductService  # <- deine überarbeitete Serviceklasse
from shop.models import Product


class AdminStockUpdaterView(APIView):
    """
    View für Superuser: Produkt nach Artikelnummer abrufen (GET) oder Lagerbestand ändern (POST)
    """
    permission_classes = [IsSuperUser]

    def get(self, request):
        article_nr = request.query_params.get("article_nr")

        if not article_nr:
            return Response({"error": "article_nr is required"}, status=status.HTTP_400_BAD_REQUEST)

        product_serializer = AdminProductService.get_product_by_article(article_nr)

        if not product_serializer:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Erwartet:
        {
            "article_nr": "ART-123",
            "new_stock": 15
        }
        """
        article_nr = request.data.get("article_nr")
        new_stock = request.data.get("new_stock")

        if not article_nr or new_stock is None:
            return Response({"error": "article_nr and new_stock are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(article_nr=article_nr)
            product.stock = new_stock
            product.save()
            return Response({"message": f"Stock for {article_nr} updated to {new_stock}"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
