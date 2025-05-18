from django.utils import timezone
from devtools import debug
from django.db import transaction

from orders.models import Order, OrderItem
from cart.models import Cart
from beautyshop.logging_config import setup_logger


class OrderCreator:
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

    def create_order(self, payment_method: str | None = None) -> Order | None:
        """
        Create a new Order object and related OrderItems based on the user's cart.

        The function checks if the user has a valid cart. If yes, it creates an Order with
        a calculated total price and individual OrderItems for each CartItem. All operations
        are wrapped in an atomic transaction to ensure database integrity.

        Returns:
            Order | None: The created Order instance or None if no cart is found.
        """
        if not self.cart:
            self.logger.info(
                f"[ORDER] Cannot create order - no cart for user: {self.user.email}."
            )
            return None

        cart_items = self.cart.items.select_related("product")

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            order = Order.objects.create(
                user=self.user,
                total_price=total_price,
                created_at=timezone.now(),
                payment_method=payment_method or "",
                payment_status=Order.PaymentStatus.OPEN,
            )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        return order
