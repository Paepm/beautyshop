from django.shortcuts import get_object_or_404
from django.db.models import F

from ..models import Product


class ProductService:
    """
    Service class for handling product-related operations.
    """

    @staticmethod
    def get_all_products(category: str = None, sale: str = None) -> list[Product]:
        """Fetch all products from the database and filter by category if provided
        and the 2. filter for products on sale.
        """
        queryset = Product.objects.all()

        if category:
            queryset = queryset.filter(category__name__iexact=category)

        if sale == "true":
            queryset = queryset.filter(
                price_old__isnull=False, price_old__gt=F("price_current")
            )
        return list(queryset)

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        """Fetch a product by its ID."""
        return get_object_or_404(Product, id=product_id)
