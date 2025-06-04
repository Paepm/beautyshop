from cart.models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()


# first static factory pattern in my life! nice to learn it
class CartManager:
    """
    Responsible for retrieving or creating a Cart instance for a given user.
    """

    @staticmethod
    def get_or_create_cart(user: User) -> Cart:
        """
        Retrieve the cart for the user, or create one if it doesn't exist.

        Args:
            user (User): The authenticated user.

        Returns:
            Cart: The user's cart.
        """
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get_existing_cart(user: User) -> Cart | None:
        """
        Retrieve the cart if it exists, or return None.

        Args:
            user (User): The authenticated user.

        Returns:
            Cart | None: The cart if found, otherwise None.
        """
        return Cart.objects.filter(user=user).first()
