from django.shortcuts import get_object_or_404
from devtools import debug

from cart.models import CartProduct
from beautyshop.logging_config import setup_logger
from shop.models import Product
from cart.services.cart_manager import CartManager
from cart.enums.cart_action import CartAction


class CartService:
    """
    Service class to encapsulate all business logic related to a user's shopping cart.
    """

    def __init__(self, user):
        """
        Initialize the CartService with the current user.

        Args:
            user (User): The authenticated user whose cart is being managed.
        """
        self.user = user
        self.cart = CartManager.get_or_create_cart(user)
        self.logger = setup_logger(__name__)

    def add_product(self, product_id: int, quantity: int = 1) -> CartProduct:
        """
        Add a product to the user's cart. Check if the total quantity (in cart + quantity) exceeds the stock.
        """
        product: Product = get_object_or_404(Product, id=product_id)

        if not product.available:
            raise ValueError("Product is not available.")

        cart_item: CartProduct = CartProduct.objects.filter(
            cart=self.cart, product=product
        ).first()

        current_quantity = cart_item.quantity if cart_item else 0
        new_quantity = current_quantity + quantity

        if new_quantity > product.stock:
            raise ValueError("Not enough stock available.")

        if cart_item:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item = CartProduct.objects.create(
                cart=self.cart, product=product, quantity=quantity
            )

        return cart_item

    def get_cart_products(self) -> list[CartProduct]:
        """
        Return all items in the user's cart.

        Returns:
            list[CartProduct]: A list of CartProduct instances or an empty list.
        """
        return self.cart.items.all()

    def get_total_price(self) -> float:
        """
        Calculate the total price of all items in the cart.
        Converte the total price to a float because the sum function returns an int.

        Returns:
            float: The total cart value.
        """
        return sum(item.model_get_total_price() for item in self.get_cart_products())

    def remove_product(self, product_id: int) -> bool:
        """
        Remove a specific item from the user's cart.

        Args:
            product_id (int): The ID of the CartItem to remove.

        Returns:
            None
        """
        try:
            item = get_object_or_404(CartProduct, id=product_id, cart=self.cart)
            item.delete()
            self.logger.info(f"Product removed: {item.product.name}")
            return True
        except Exception as e:
            self.logger.warning(f"Failed to remove product {product_id}: {e}")
            return False

    def update_quantity(
        self, product_id: int, action: str = None, quantity: int = None
    ) -> bool:
        """
        Update the quantity of a specific cart item, either by increment/decrement or a direct input.
        Checks if the product is not out of stock before let user updating the quantity.

        Args:
            product_id (int): The ID of the CartItem to update.
            action (str, optional): 'increment' or 'decrement' to adjust quantity.
            quantity (str, optional): Directly set a quantity value (from form input).

        Returns:
            Bool: True if the update was successful, False otherwise.
        """
        try:
            item = get_object_or_404(CartProduct, id=product_id, cart=self.cart)

            if action == CartAction.INCREMENT.value:
                if item.product.stock <= item.quantity:
                    self.logger.warning(
                        f"Cannot increment quantity for {item.product.name}, stock limit reached."
                    )
                    return False
                item.quantity += 1
            elif action == CartAction.DECREMENT.value:
                item.quantity = max(1, item.quantity - 1)
            elif quantity:
                item.quantity = max(1, int(quantity))

            item.save()
            self.logger.info(f"Updated quantity for item {product_id}: {item.quantity}")
            return True

        except Exception as e:
            self.logger.warning(f"Failed to update quantity for item {product_id}: {e}")
            return False

    def clear_cart(self) -> None:
        """
        Clear all items from the user's cart.
        """
        if self.cart:
            self.cart.items.all().delete()
