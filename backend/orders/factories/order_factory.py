from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from orders.models import Order, OrderItem
from orders.enums.paymentstatus import PaymentStatus
from orders.enums.orderstatus import OrderStatus


class OrderFactory:
    """
    Factory class responsible for creating orders from cart data.
    """

    def __init__(self, user, cart):
        self.user = user
        self.cart = cart

    def create(
        self,
        payment_provider: str | None = None,
        shipping_data: dict | None = None,
        payment_method: str = "standard",
    ) -> Order | None:

        if not self.cart:
            return None

        cart_items = self.cart.items.select_related("product")
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        shipping_cost = Decimal(4.90 if payment_method == "standard" else 9.90)

        with transaction.atomic():
            order = Order.objects.create(
                user=self.user,
                total_price=total_price + shipping_cost,
                created_at=timezone.now(),
                payment_provider=payment_provider,
                payment_status=PaymentStatus.OPEN,
                order_status=OrderStatus.PENDING,
                shipping_address=shipping_data.get("address", ""),
                shipping_post_code=shipping_data.get("post_code", ""),
                shipping_city=shipping_data.get("city", ""),
                shipping_country=shipping_data.get("country", ""),
                shipping_method=payment_method,
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
