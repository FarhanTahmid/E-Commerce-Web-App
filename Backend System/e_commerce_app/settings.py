"""
Django settings for e_commerce_app project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('SETTINGS')=='dev':
    DEBUG = True
else:
    DEBUG = False
 
if os.environ.get('SETTINGS')=='dev':
    ALLOWED_HOSTS = ['*']
else:
    pass


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'system',
    'business_company',
    'products',
    'inventory',
    'customer',
    'orders',
    'business_admin',
    'server_api',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_commerce_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_commerce_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if os.environ.get('SETTINGS')=='dev':

    DATABASES = {
        # Sqlite
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / 'db.sqlite3',
        # }
        
        # POSTGRESQL
        'default': {
                #Postgres in localhost
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DEV_DATABASE_NAME'),
                'USER': os.environ.get('DEV_DATABASE_USER'),
                'PASSWORD': os.environ.get('DEV_DATABASE_PASSWORD'),
                'HOST': os.environ.get('DEV_DATABASE_HOST'),
                'PORT':'5432', 
        }
    }
    
else:
    # Use Production Database Here
    pass


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

from django.utils import timezone
TIME_ZONE = os.environ.get('TIME_ZONE')

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

if os.environ.get('SETTINGS')=='dev':
    STATIC_URL = 'static/'
    # Static Root
    STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
    # Static Files Directory
    STATICFIlES_DIRS=(os.path.join(BASE_DIR,'static/'))

    # Media files
    MEDIA_ROOT= os.path.join(BASE_DIR, 'Media/')
    MEDIA_URL= "/media_files/"
else:
    # USE AWS Or production static file server
    pass



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # AWS Configs for production usage
# AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY')
# AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

# # S3 Configs
# AWS_STORAGE_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME')
# DEFAULT_FILE_STORAGE=os.environ.get('DEFAULT_FILE_STORAGE')
# STATICFILES_STORAGE=os.environ.get('STATICFILES_STORAGE')
# AWS_S3_CUSTOM_DOMAIN='%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME