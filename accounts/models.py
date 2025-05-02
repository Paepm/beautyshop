from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class CustomUser(AbstractUser):
    country = CountryField(blank_label='select country', null=True, blank=True),
    city = models.CharField(max_length=100, null=True, blank=True),
    address = models.CharField(max_length=255, null=True, blank=True),
    postal_code = models.CharField(max_length=20, null=True, blank=True),
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username
    
    