from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from devtools import debug

from ..serializer.serializers import ProductSerializer
from ..services.product_service import ProductService


class ProductListView(APIView):
    """
    API view to list all products.
    """

    def get(self, request) -> Response:
        """
        Handle GET requests to retrieve all products.
        """
        category = request.query_params.get("category")
        sale = request.query_params.get("sale")
        available = request.query_params.get("available")
        # debug("AVAILABLE IN VIEW", available)
        products = ProductService.get_all_products(
            category=category, sale=sale, available=available
        )
        serializer = ProductSerializer(products, many=True)
        # debug("SERIALIZER DATA", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """
    API view to retrieve a product by its ID.
    """

    def get(self, request, product_id) -> Response:
        """
        Handle GET requests to retrieve a product by its ID.
        """
        product = ProductService.get_product_by_id(product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
