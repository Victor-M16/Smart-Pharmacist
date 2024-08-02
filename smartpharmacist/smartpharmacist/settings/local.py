from smartpharmacist.settings.base import *

DEBUG = True

DATABASES = {
    "default":{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartpharmacist', 
        'USER':'root',      
        'PASSWORD': 'mjima',  
        'HOST': '127.0.0.1',
        'PORT': '3306',     
    }
}



