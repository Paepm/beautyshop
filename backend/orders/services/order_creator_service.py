from devtools import debug
from beautyshop.logging_config import setup_logger

from cart.models import Cart
from orders.factories.order_factory import OrderFactory
from orders.models import Order


class OrderCreatorService:
    """Responsible for creating an Order and related OrderItems from a user's cart"""

    def __init__(self, user):
        """Initialize the OrderCreator with a user and attempt to retrieve their cart."""
        self.user = user
        self.cart = self._get_cart()
        self.logger = setup_logger(__name__)

    def _get_cart(self) -> Cart | None:
        """
        Attempt to retrieve the current user's cart from the database.

        If a cart exists, it is returned. If not, the function returns None.
        This is a helper function and should not be called from outside the class.

        Returns:
            Cart | None: The cart instance if found, otherwise None.
        """
        try:
            cart = Cart.objects.get(user=self.user)
            return cart

        except Cart.DoesNotExist:
            self.logger.warning(f"[CART] No cart found for user: {self.user.email}")
            return None

    def create_order(
        self, payment_provider, shipping_data, payment_method
    ) -> Order | None:
        """
        Use the OrderFactory to create an Order from the user's cart.

        Return:
             Order | None: The created Order instance if successful, otherwise None.
        """
        if not self.cart:
            self.logger.error(
                f"[ORDER_CREATOR] No cart found for user: {self.user.email}"
            )
            return None

        factory = OrderFactory(user=self.user, cart=self.cart)

        return factory.create(
            payment_provider=payment_provider,
            shipping_data=shipping_data,
            payment_method=payment_method,
        )
