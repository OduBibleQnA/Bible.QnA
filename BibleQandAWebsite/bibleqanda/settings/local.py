from .base import *
from os import environ
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / "bibleqanda" / "settings" / ".env")

SECRET_KEY = "django-insecure-ym*t!mlxgh@1e9uvp4+v%8#37hzy5%_$ip7$2&b3vd**w4v^&r"

DEBUG = True

ALLOWED_HOSTS = []

ENCRYPTION_KEY = get_secret()

environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

PASSWORD_RESET_TIMEOUT = 60 * 30

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/Users/steve/Desktop/BibleQandAWebsite/cache/django_cache",
    }
}

CORS_ALLOW_ALL_ORIGINS = True