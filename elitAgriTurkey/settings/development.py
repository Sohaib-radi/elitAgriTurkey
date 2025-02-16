from .base import *

# Debug mode for development
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ['localhost', '127.0.0.1','63.250.41.35']

# Database configuration for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'