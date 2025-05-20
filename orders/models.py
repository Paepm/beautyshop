from django.db import models
from django.conf import settings

from cart.models import CartItem
from shop.models import Item as product
from payments.enums.payment_methods import PaymentMethod
from orders.enums.paymentstatus import PaymentStatus
from orders.enums.orderstatus import OrderStatus


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255, blank=True, default="")

    # get the payment methods from the payment_methods.py Enum and convert to a list of tuples
    payment_method = models.CharField(
        choices=[(e.value, e.name.title()) for e in PaymentMethod], max_length=30
    )

    payment_status = models.CharField(
        choices=PaymentStatus.choices, default=PaymentStatus.OPEN, max_length=30
    )

    order_status = models.CharField(
        choices=OrderStatus.choices, default=OrderStatus.PENDING, max_length=30
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user} – {self.payment_status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # item price at order time
