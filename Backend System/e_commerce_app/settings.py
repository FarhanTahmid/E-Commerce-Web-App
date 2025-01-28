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
    'system',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_api_key',
    'corsheaders',
    'storages',
    'business_company',
    'products',
    'inventory',
    'orders',
    'customer',
    'business_admin',
    'server_api',
    'client_api',
    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend domain
    "http://192.168.68.109:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-api-key",
]
REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework_api_key.permissions.HasAPIKey',
    ],
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}



CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://192.168.68.109:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
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

AUTH_USER_MODEL = "system.Accounts"

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
# ]


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