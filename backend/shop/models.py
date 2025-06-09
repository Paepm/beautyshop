from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    price_purchase = models.DecimalField(  # Einkaufspreis (intern)
        max_digits=10, decimal_places=2
    )
    price_old = models.DecimalField(  # früherer Preis (für Rabattanzeige)
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    price_current = models.DecimalField(  # aktueller Preis
        max_digits=10, decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: SEO, Slug, Meta
    slug = models.SlugField(unique=True, blank=True)

    @property
    def sale(self):
        """
        sale = True, when price_old is set and greater than price_current.
        sale is used to show a product as discounted.

        """
        return self.price_old is not None and self.price_old > self.price_current

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.available = self.stock > 0

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
