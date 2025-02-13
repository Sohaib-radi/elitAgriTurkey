from .base import *

# Debug mode for development
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ['*']

# Database configuration for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'elitagri',           
        'USER': 'adminDb',            
        'PASSWORD': 'iW}B$i4vBy{BL["}',   
        'HOST': '63.250.41.35',           
        'PORT': '5432',               
    }
}

# Static files configuration for development
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'