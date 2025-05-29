from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ItemSerializer

from .models import Product


@api_view(["GET"])
def api_product_list(request):
    items = Product.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
