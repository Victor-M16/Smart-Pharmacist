from .base_settings import *

DATABASES = {
    "default":{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway', 
        'USER':'root',      
        'PASSWORD': 'HTNKkrwmUcDSQFPyKERTkubRWPDXqCuB',  
        'HOST': 'mysql.railway.internal',
        'PORT': '3306',     
    }
}