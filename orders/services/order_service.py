from django.utils import timezone  
from devtools import debug
from orders.models import Order, OrderItem
from cart.models import Cart

class OrderService:

    def __init__(self, user):
        self.user = user
        self.cart = self._get_cart()

    def _get_cart(self) -> Cart | None:
        try:
            return Cart.objects.get(user=self.user)
        
        except Cart.DoesNotExist:
            return None


    def create_order(self) -> Order:
        if not self.cart:
            return None
        
        cart_items = self.cart.items.select_related('product')
        # debug(cart_items)
        total_price = sum(item.get_total_price() for item in cart_items)

        order: Order = Order.objects.create(user=self.user, created_at=timezone.now(), status='pending', total_price=total_price)
        
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        
        self.clear_cart()
        return order
    
    
    def clear_cart(self):
        self.cart.items.all().delete()

