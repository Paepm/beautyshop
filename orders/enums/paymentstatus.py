from django.db import models


# models.TextChoices is a Enum class for django models that allows me to use choices to find all values of the enum
class PaymentStatus(models.TextChoices):
    OPEN = "open", "Open"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    EXPIRED = "expired", "Expired"
