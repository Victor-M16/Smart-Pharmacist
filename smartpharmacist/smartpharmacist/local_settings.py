from .base_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartpharmacist', 
        'USER':'postgres',      
        'PASSWORD': 'mjima',  
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
