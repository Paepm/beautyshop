from django.utils import timezone
from devtools import debug
from django.db import transaction
from decimal import Decimal

from orders.models import Order, OrderItem
from cart.models import Cart
from beautyshop.logging_config import setup_logger
from orders.enums.paymentstatus import PaymentStatus
from orders.enums.orderstatus import OrderStatus


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

    def create_order(
        self,
        payment_provider: str | None = None,
        shipping_data: dict | None = None,
        shipping_method: str = "standard",
    ) -> Order | None:
        """
        Create a new Order object and related OrderItems based on the user's cart,
        including optional shipping data and selected shipping method.

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
        debug("[ORDER_CREATOR] Total price calculated:", total_price)

        shipping_cost = Decimal(4.90 if shipping_method == "standard" else 9.90)
        debug("[ORDER_CREATOR] Shipping cost determined:", shipping_cost)

        with transaction.atomic():
            order = Order.objects.create(
                user=self.user,
                total_price=total_price + shipping_cost,
                created_at=timezone.now(),
                payment_provider=payment_provider if payment_provider else None,
                payment_status=PaymentStatus.OPEN,
                order_status=OrderStatus.PENDING,
                shipping_address=shipping_data.get("address") if shipping_data else "",
                shipping_post_code=(
                    shipping_data.get("post_code") if shipping_data else ""
                ),
                shipping_city=shipping_data.get("city") if shipping_data else "",
                shipping_country=shipping_data.get("country") if shipping_data else "",
                shipping_method=shipping_method,
                shipping_cost=shipping_cost,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

        return order
