from .common import *


SECRET_KEY = "django-insecure-lg356n@3l^i3e9ggcf*03tvcf0w-vak#$)l%z6j+_=(yo)a7&6"


DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "anees",
        "USER": "postgres",
        "PASSWORD": "bassiony",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "email@gmail.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_TLS = True



# INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = [
    "127.0.0.1",
]

DOMAIN = "localhost:5000"


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]
