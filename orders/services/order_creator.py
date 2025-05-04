from django.utils import timezone  
from devtools import debug
from orders.models import Order, OrderItem
from cart.models import Cart

class OrderCreator:
    """"Responsible for creating an Order and related OrderItems from a user's cart"""

    def __init__(self, user):
        self.user = user
        self.cart = self._get_cart()

    def _get_cart(self) -> Cart | None:
        """
        Attempt to retrieve the current user's cart from the database.

        If a cart exists, it is returned. If not, the function returns None.
        This is a helper function and should not be called from outside the class.

        Returns:
            Cart | None: The cart instance if found, otherwise None.
        """
        try:
            return Cart.objects.get(user=self.user)
        
        except Cart.DoesNotExist:
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
            return None
        
        cart_items = self.cart.items.select_related('product')
        
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order: Order = Order.objects.create(user=self.user, created_at=timezone.now(), status='pending', total_price=total_price)
        
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        
        return order
    


