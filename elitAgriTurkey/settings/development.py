from .base import *

# Debug mode for development
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ['*']

# Database configuration for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files configuration for development
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'