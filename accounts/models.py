from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.contrib.auth.models import BaseUserManager


# class is needed to handle user and superuser creations --> django does not know how to handle the superuser when customUser gets created
# CustomUserManager is needed to handle the creation of users and superusers
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    # Create CustomUser
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create the superuser
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)
    
# # CustomUser model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    country = CountryField(blank_label='select country', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    objects = CustomUserManager()

    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female')],
        blank=True
    )
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    newsletter_opt_in = models.BooleanField(default=False)
    terms_accepted = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    