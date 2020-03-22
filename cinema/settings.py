"""
Django settings for cinema project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ly@(o2*t7io4$mj8v440%sg&#y9g0oui8@d44*s#9)k10j9!y%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'client.apps.ClientConfig',
    'worker.apps.WorkerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    # 'django_celery_beat',  # https://djangopy.org/how-to/handle-asynchronous-tasks-with-celery-and-django
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
        'NAME': 'cinema_db',
        # 'NAME': 'cinema_2',
        'USER': 'postgres',
        'PASSWORD': 'licencjat123!',
        # 'HOST': 'localhost',
        'HOST': '80.211.204.44',
        'PORT': '5432',
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# potrzebne, aby działały skrypty js
# python manage.py collectstatic zbiera statyczne pliki do jednego folderu
# tutaj wskazujemy sciezki do plikow statycznych w aplikacjach
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'worker', "static"),
    os.path.join(BASE_DIR, 'client', "static"),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_REDIRECT_URL = 'panel'  # przekieowanie po zalogowaniu
LOGIN_URL = 'main'  # kiedy chemy sie dostac do sciezki niedostepnej bez logowania to przekierowuje na ten adres url
LOGOUT_REDIRECT_URL = 'main'  # przekierowanie po wykogowaniu

# mail data
# https://support.google.com/mail/answer/7126229?hl=pl

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'moviecitycinema@gmail.com'
EMAIL_HOST_PASSWORD = 'Licencjat123!'
EMAIL_USE_TLS = True
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'sender@localhost'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
