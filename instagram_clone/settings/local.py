from django.core.management.utils import get_random_secret_key
from .base import *
from .env import env, BASE_DIR
import os

INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_authtoken',
    'storages',
    'drf_spectacular',
    'silk',
    'authentication_app.apps.AuthenticationAppConfig',
    'post_management_app.apps.PostManagementAppConfig',
    'user_management_app.apps.UserManagementAppConfig',
]

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
]

DEBUG = env.bool('DJANGO_DEBUG', default=True)
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default=get_random_secret_key())

ALLOWED_HOSTS = []

TIME_ZONE = env('TIME_ZONE', default='Asia/Kolkata')

DATABASES = {
    'default':{
        'ENGINE': env('DB_ENGINE', default='django.db.backends.postgresql'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Instagram Backend Using Django',
    'DESCRIPTION': 'This is a practice project of Django REST Framework(DRF).',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/api/',
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'