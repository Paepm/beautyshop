from django.db import models


# models.TextChoices is a Enum class for django models that allows me to use choices to find all values of the enum
class OrderStatus(models.TextChoices):
    OPEN = "open", "Open"
    PENDING = "pending", "Pending"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELED = "canceled", "Canceled"
    REFUNDED = "refunded", "Refunded"
    RETURNED = "returned", "Returned"
    PROCESSING = "processing", "Processing"
