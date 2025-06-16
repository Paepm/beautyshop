from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from shop.models import Product as product
from payments.enums.payment_providers import PaymentProviders
from orders.enums.paymentstatus import PaymentStatus
from orders.enums.orderstatus import OrderStatus
from orders.enums.shipping_providers import ShippingProviderChoices


class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # shipping details
    shipping_first_name = models.CharField(max_length=100, blank=False, null=False)
    shipping_last_name = models.CharField(max_length=100, blank=False, null=False)
    shipping_address = models.CharField(
        max_length=255,
        blank=False,
        null=True,
    )
    shipping_post_code = models.CharField(
        max_length=20,
        blank=False,
        null=True,
    )
    shipping_city = models.CharField(
        max_length=100,
        blank=False,
        null=True,
    )
    shipping_country = models.CharField(
        max_length=100,
        blank=False,
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

    # invoice details
    invoice_address = models.CharField(max_length=255, blank=False, null=False)
    invoice_post_code = models.CharField(max_length=20, blank=False, null=False)
    invoice_city = models.CharField(max_length=100, blank=False, null=False)
    invoice_country = models.CharField(max_length=100, blank=False, null=False)
    invoice_first_name = models.CharField(max_length=100, blank=False, null=False)
    invoice_last_name = models.CharField(max_length=100, blank=False, null=False)

    # shipping provider data
    tracking_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Tracking ID for the shipment, if available",
    )
    tracking_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="URL to track the shipment, if available",
    )
    shipping_provider = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        choices=ShippingProviderChoices.choices,
        help_text="The shipping provider handling this order",
    )
    last_tracking_update = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time the tracking information was updated",
    )
    delivery_estimate = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Estimated delivery time for the order",
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

    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user} – {self.payment_status}"

    # JUST FOR TESTING PURPOSES
    def is_ready_for_delivery_mark(self):
        if self.order_status != "shipped":
            return False
        if not self.updated_at:
            return False
        return self.updated_at <= timezone.now() - timedelta(minutes=5)

    def get_payment_provider_label(self):
        try:
            return PaymentProviders(self.payment_provider).label
        except ValueError:
            return self.payment_provider  # fallback


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_current = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # item price at order time
