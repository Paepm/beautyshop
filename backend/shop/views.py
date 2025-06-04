from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializer.serializers import ProductSerializer
from .models import Product
from devtools import debug


@api_view(["GET"])
def product_list(request):
    items = Product.objects.all()
    serializer = ProductSerializer(items, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail_view(request, pk):
    debug(f"Fetching product with primary key: {pk}")
    try:
        product = Product.objects.get(pk=pk)
        debug(f"Product found: {product.name}")
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSerializer(product)
    return Response(serializer.data)
