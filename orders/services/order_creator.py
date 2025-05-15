from django.utils import timezone  
from devtools import debug

from orders.models import Order, OrderItem
from cart.models import Cart
from beautyshop.logging_config import setup_logger

logger = setup_logger(__name__)

class OrderCreator:
    """Responsible for creating an Order and related OrderItems from a user's cart"""

    def __init__(self, user):
        """Initialize the OrderCreator with a user and attempt to retrieve their cart."""
        self.user = user
        self.cart = self._get_cart()
        logger.debug(f'[INIT] OrderCreator initialized for user: {self.user.email}.')

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
            logger.debug(f'[CART] Cart found for user: {self.user.email}.')
            return cart
        
        except Cart.DoesNotExist:
            logger.warning(f'[CART] No cart found for user: {self.user.email}')
            return None


    def create_order(self) -> Order | None:
        """
        Create a new Order object and related OrderItems based on the user's cart.

        The function checks if the user has a valid cart. If yes, it creates an Order with 
        a calculated total price and individual OrderItems for each CartItem. All operations 
        are wrapped in an atomic transaction to ensure database integrity.

        Returns:
            Order | None: The created Order instance or None if no cart is found.
        """
        if not self.cart:
            logger.info(f'[ORDER] Cannot create order - no cart for user: {self.user.email}.')
            return None
        
        cart_items = self.cart.items.select_related('product')
        
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order: Order = Order.objects.create(user=self.user, created_at=timezone.now(), payment_status='pending', total_price=total_price)
        logger.info(f'[ORDER] Order created for user: {self.user.email} with total price: {total_price} €.')
        
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            logger.debug(f'[ORDER ITEM] Added product {item.product.name} x{item.quantity} to order #{order.id}')
        
        return order
    


