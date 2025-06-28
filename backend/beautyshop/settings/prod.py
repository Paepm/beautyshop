# backend/beautyshop/settings/prod.py
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

FRONTEND_BASE_URL = "https://coffee-crew.at"

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
CORS_ALLOWED_ORIGINS = [
    "https://coffee-crew.at",
    "https://www.coffee-crew.at",
]
CORS_ALLOW_ALL_ORIGINS = False  # ❗ WICHTIG

# Weitere Security-Einstellungen
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_SSL_REDIRECT = True
