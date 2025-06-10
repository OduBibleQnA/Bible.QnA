from .base import *
from bibleqanda.settings import get_secret

SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ["*"]
PASSWORD_RESET_TIMEOUT = 60 * 10

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
if get_secret("USE_POSTGRES", "false") == "false":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=get_secret("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }

# Cache
if get_secret("CACHE_UP", "false") == "true":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": get_secret("MEMCACHED_LOCATION", "127.0.0.1:11211"),
        }
    }
else:
    # temporary
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": "/cache/django_cache",
        }
    }


# TEMP UNTIL GET SITE:
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "https://yourapp.com"]