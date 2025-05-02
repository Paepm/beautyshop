from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from cart.models import CartItem
from shop.models import Item as product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='pending', max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # order total price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)    # item price at order time

