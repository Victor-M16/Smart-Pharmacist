from .base_settings import *

DATABASES = {
    "default":{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartpharmacist', 
        'USER':'root',      
        'PASSWORD': 'mjima',  
        'HOST': 'localhost',
        'PORT': '3306',     
    }
}


NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
