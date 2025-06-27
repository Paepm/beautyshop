import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "backend",
    "62.178.83.52",
    "192.168.0.11",
    "coffee-crew.at",
    "www.coffee-crew.at",
]

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "beautyshop"),
        "USER": os.environ.get("POSTGRES_USER", "beautyshop_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "beautyshop_pass"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    "https://coffee-crew.at",
    "https://www.coffee-crew.at",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # ggf. später einschränken
