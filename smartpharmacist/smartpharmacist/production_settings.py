import os
from .base_settings import *  # Import base settings
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL")
    )
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
CSRF_TRUSTED_ORIGINS = ['https://smart-pharmacist-production.up.railway.app', 'https://192.168.8.124:443',]


# Configure CORS for API
CORS_ALLOW_ALL_ORIGINS = True

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
