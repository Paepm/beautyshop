from django.db.models import Sum
from django.shortcuts import get_object_or_404
from devtools import debug

from cart.models import Cart, CartItem

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
        self.cart = self._get_cart()

    def _get_cart(self) -> Cart | None:
        """
        Attempt to retrieve the user's cart from the database.

        Returns:
            Cart | None: The Cart instance if it exists, otherwise None.
        """
        try:
            return Cart.objects.get(user=self.user)
        except Cart.DoesNotExist:
            return None
        
    def get_cart_items(self) -> list[CartItem]:
        """
        Return all items in the user's cart.

        Returns:
            list[CartItem]: A list of CartItem instances or an empty list.
        """
        return self.cart.items.all() if self.cart else []
    
    def get_total_price(self)-> float:
        """
        Calculate the total price of all items in the cart.
        Converte the total price to a float because the sum function returns an int.

        Returns:
            float: The total cart value.
        """
        return sum(item.model_get_total_price() for item in self.get_cart_items())
    
    def remove_item(self, item_id: int) -> None:
        """
        Remove a specific item from the user's cart.

        Args:
            item_id (int): The ID of the CartItem to remove.

        Returns:
            None
        """
        if self.cart:
            item: CartItem = get_object_or_404(CartItem, id=item_id, cart=self.cart)
            item.delete()

    def update_quantity(self, item_id: int, action: str=None, quantity: int=None) -> None:
        """
        Update the quantity of a specific cart item, either by increment/decrement or a direct input.

        Args:
            item_id (int): The ID of the CartItem to update.
            action (str, optional): 'increment' or 'decrement' to adjust quantity.
            quantity (str, optional): Directly set a quantity value (from form input).

        Returns:
            None
        """
        if not self.cart:
            return
        
        item: CartItem = get_object_or_404(CartItem, id=item_id, cart=self.cart)

        if action == 'increment':
            item.quantity += 1
        elif action == 'decrement':
            item.quantity -= 1
        elif quantity:
            try:
                item.quantity = max(1, int(quantity))  # Ensure quantity doesn't go below 1
            except ValueError:
                return  # Handle invalid quantity input
        item.save()