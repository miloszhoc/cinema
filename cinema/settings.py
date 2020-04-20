"""
Django settings for cinema project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# sendgrid backend
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'client.apps.ClientConfig',
    'worker.apps.WorkerConfig',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'storages',  # https://pypi.org/project/django-storages-azure/#description'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cinema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cinema.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pl-pl'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOGIN_REDIRECT_URL = 'panel'  # przekieowanie po zalogowaniu
LOGIN_URL = 'main'  # kiedy chemy sie dostac do sciezki niedostepnej bez logowania to przekierowuje na ten adres url
LOGOUT_REDIRECT_URL = 'main'  # przekierowanie po wykogowaniu

# sendgrid
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

# https://stackoverflow.com/questions/54729137/django-azure-upload-file-to-blob-storage
# azure storage config
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
AZURE_CUSTOM_DOMAIN = os.environ.get('AZURE_CUSTOM_DOMAIN')
AZURE_LOCATION = os.environ.get('AZURE_LOCATION')
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER')

DEFAULT_FILE_STORAGE = 'cinema.custom_azure.AzureMediaStorage'
MEDIA_URL = 'https://{}/media/'.format(AZURE_CUSTOM_DOMAIN)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# python manage.py collectstatic zbiera statyczne pliki do jednego folderu
STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# STATIC_URL = '/static/'
STATIC_URL = 'https://{}/static/'.format(AZURE_CUSTOM_DOMAIN)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
