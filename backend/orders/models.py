from django.db import models
from django.conf import settings

from cart.models import CartProduct
from shop.models import Product as product
from payments.enums.payment_providers import PaymentProviders
from orders.enums.paymentstatus import PaymentStatus
from orders.enums.orderstatus import OrderStatus


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    shipping_post_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    shipping_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    shipping_country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    shipping_method = models.CharField(
        max_length=50,
        default="standard",
        help_text="Shipping method chosen by the user (e.g. standard, express)",
    )
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Shipping cost for the order in €",
    )

    # get the payment_method from the webhook dict from stripe or paypal
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Set after successful checkout (e.g. card, klarna, google_pay)",
    )

    # get the payment_provider from the provicer_payment_method.py Enum and convert to a list of tuples
    payment_provider = models.CharField(
        choices=[(e.value, e.name.title()) for e in PaymentProviders],
        max_length=80,
        # default=PaymentProvider.STRIPE.value,
    )

    payment_status = models.CharField(
        choices=PaymentStatus.choices, default=PaymentStatus.OPEN, max_length=30
    )

    order_status = models.CharField(
        choices=OrderStatus.choices, default=OrderStatus.PENDING, max_length=30
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user} – {self.payment_status}"

    def get_payment_provider_label(self):
        try:
            return PaymentProviders(self.payment_provider).label
        except ValueError:
            return self.payment_provider  # fallback


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # item price at order time
