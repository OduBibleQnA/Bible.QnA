from .base import *
from bibleqanda.settings import get_secret

SECRET_KEY = get_secret("SECRET_KEY")
ENCRYPTION_KEY = get_secret("ENCRYPTION_KEY")

DEBUG = False
raw_hosts = get_secret("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [host.strip() for host in raw_hosts.split(",") if host.strip()]
PASSWORD_RESET_TIMEOUT = 60 * 10

EMAIL_BACKEND = get_secret("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = get_secret("EMAIL_HOST")
EMAIL_PORT = int(get_secret("EMAIL_PORT", 587))
EMAIL_USE_TLS = get_secret("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = get_secret("DEFAULT_FROM_EMAIL", f"Bible Q&A <{EMAIL_HOST_USER}>")

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': f"django.db.backends.{get_secret("DATABASE_ENGINE", "sqlite3")}",
        'NAME': get_secret("DATABASE_NAME", "bibleqna"),
        'USER':get_secret("DATABASE_USERNAME", 'admin'),
        'PASSWORD':get_secret('DATABASE_PASSWORD', "admin"),
        'HOST':get_secret('DATABASE_HOST', 'db'),
        'PORT':get_secret("DATABASE_PORT", 5432)
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{get_secret('REDIS_HOST', 'redis')}:6379/15",
        "OPTIONS": {
            "IGNORE_EXCEPTIONS": True,  # Acts like memcached: fail silently
        },
    }
}


SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CORS_ALLOW_ALL_ORIGINS = bool(get_secret("CORS_ALLOW_ALL_ORIGINS", 0))
CORS_ALLOW_NULL_ORIGIN = bool(get_secret("CORS_ALLOW_NULL_ORIGIN", 1))
CORS_ALLOWED_ORIGINS = [get_secret("CORS_ALLOWED_ORIGINS", "")]
