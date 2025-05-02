from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True);
    email = models.EmailField(unique=True);
    password1 = models.CharField(max_length=128);
    password2 = models.CharField(max_length=128);
    country = CountryField(blank_label='select country', null=True, blank=True);
    city = models.CharField(max_length=100, null=True, blank=True);
    address = models.CharField(max_length=255, null=True, blank=True);
    post_code = models.CharField(max_length=20, null=True, blank=True);
    phone_number = models.CharField(max_length=20, null=True, blank=True);

    def __str__(self):
        return self.username
    
    