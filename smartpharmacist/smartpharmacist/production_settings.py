import os
from .base_settings import *  # Import base settings

DEBUG = False

ALLOWED_HOSTS = ['*']

# Use SQLite for now
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (if you have any)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tailwind settings
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]

# Other production-specific settings
CSRF_TRUSTED_ORIGINS = ['https://smart-pharmacist-production.up.railway.app']

# Configure CORS for API
CORS_ALLOWED_ORIGINS = ['https://smart-pharmacist-production.up.railway.app']
