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
        invoice_data: dict | None = None,
        payment_method: str = "standard",
    ) -> Order | None:

        if not self.cart:
            return None

        # just allow specific countries for shipping
        allowed_countries = {"AT", "DE", "LI", "CH"}
        country_code = (shipping_data or {}).get("country", "").upper()
        if country_code not in allowed_countries:
            raise ValueError("Shipping to this country is not available.")

        # check if the cart has items and if all products have sufficient stock
        cart_items = self.cart.items.select_related("product")
        for item in cart_items:
            if item.product.stock < item.quantity:
                raise ValueError(
                    f"{item.product.name} is out of stock or insufficient stock for quantity {item.quantity}."
                )

        total_price = sum(
            item.product.price_current * item.quantity for item in cart_items
        )
        shipping_cost = Decimal(4.90 if payment_method == "standard" else 9.90)

        with transaction.atomic():
            order = Order.objects.create(
                user=self.user,
                total_price=total_price + shipping_cost,
                created_at=timezone.now(),
                payment_provider=payment_provider,
                payment_status=PaymentStatus.OPEN,
                order_status=OrderStatus.OPEN,
                shipping_first_name=shipping_data.get("first_name", ""),
                shipping_last_name=shipping_data.get("last_name", ""),
                shipping_address=shipping_data.get("address", ""),
                shipping_post_code=shipping_data.get("post_code", ""),
                shipping_city=shipping_data.get("city", ""),
                shipping_country=shipping_data.get("country", ""),
                shipping_method=payment_method,
                shipping_cost=shipping_cost,
                invoice_first_name=invoice_data.get("first_name", ""),
                invoice_last_name=invoice_data.get("last_name", ""),
                invoice_address=invoice_data.get("address", ""),
                invoice_post_code=invoice_data.get("post_code", ""),
                invoice_city=invoice_data.get("city", ""),
                invoice_country=invoice_data.get("country", ""),
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_current=item.product.price_current,
                )

        return order
