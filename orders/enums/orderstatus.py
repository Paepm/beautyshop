from django.db import models


# models.TextChoices is a Enum class for django models that allows me to use choices to find all values of the enum
class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"
    REFUNDED = "refunded", "Refunded"
    RETURNED = "returned", "Returned"
    FAILED = "failed", "Failed"
    PROCESSING = "processing", "Processing"
