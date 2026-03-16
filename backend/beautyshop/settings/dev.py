# backend/beautyshop/settings/dev.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "1753-62-178-83-52.ngrok-free.app",  # Dein ngrok dev Host
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "beautyshop",
        "USER": "beautyshop_user",
        "PASSWORD": "beautyshop_pass",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

FRONTEND_BASE_URL = "http://localhost:3000"


# CORS und CSRF für localhost:3000 (React dev server)
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
