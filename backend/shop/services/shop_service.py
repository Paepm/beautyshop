from django.shortcuts import get_object_or_404

from shop.models import Product
from cart.models import Cart, CartProduct


class ShopService:
    """
    Service class for handling shopping-related logic, such as adding products to the cart.
    """

    def __init__(self, user):
        """
        Initialize the service with the current user.

        Args:
            user (CustomUser): The authenticated user for whom the service actions apply.
        """
        self.user = user

    def add_to_cart(self, product_id: int) -> CartProduct:
        """
        Add a product to the user's cart. If the product is already present, increase the quantity.
        Otherwise, create a new CartItem for the product.

        Args:
            product_id (int): The ID of the product to be added to the cart.

        Returns:
            CartItem: The created or updated cart item.
        """
        product: Product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=self.user)

        # Check if the cart already exists, if not, create a new one
        cart_item: CartProduct = CartProduct.objects.filter(
            cart=cart, product=product
        ).first()

        if cart_item:
            # if found, increase the quantity
            cart_item.quantity += 1
        else:
            # if not found, create a new cart item
            cart_item = CartProduct.objects.create(cart=cart, product=product)

        cart_item.save()
        return cart_item
