from django.shortcuts import get_object_or_404

from ..models import Product


class ProductService:
    """
    Service class for handling product-related operations.
    """

    @staticmethod
    def get_all_products() -> list[Product]:
        """Fetch all products from the database."""
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        """Fetch a product by its ID."""
        return get_object_or_404(Product, id=product_id)
