from devtools import debug

from shop.models import Product
from ..serializers.serializers import AdminProductSerializer


class AdminProductService:
    def __init__(self):
        pass

    @staticmethod
    def get_product_by_article(article_nr: str) -> AdminProductSerializer:
        try:
            product = Product.objects.get(article_nr=article_nr)
            serializer = AdminProductSerializer(product)
        except Product.DoesNotExist:
            debug(f"No product: {article_nr} found in the database.")

        return serializer
