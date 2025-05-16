from django.db import models
from django.conf import settings

from cart.models import CartItem
from shop.models import Item as product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # order total price
    shipping_address = models.CharField(max_length=255, blank=True, default="")
    payment_method = models.CharField(choices=[
            ('card', 'Credit Card'),
            ('paypal', 'PayPal'),
            ('invoice', 'Invoice'),
            ('bank_transfer', 'Bank Transfer'),
            ('crypto', 'Crypto'),
            ('klara', 'Klara'),
    ], default='', max_length=30)
    payment_status = models.CharField(choices=[
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], default='open', max_length=30)

   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)    # item price at order time

