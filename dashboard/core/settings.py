# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from unipath import Path
import dj_database_url
import dj_database_url
from django.utils import timezone
import datetime
# sudo lsof -t -i tcp:8000 | xargs kill -9 if port in use
# Build paths ddddd inside test the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['abdebf4487d9.ngrok.io','119.59.112.130','seeoil-box.thddns.net','192.168.1.167','localhost', '127.0.0.1', '192.168.1.166', config('SERVER', default='127.0.0.1')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'linebot.apps.LinebotConfig',
    'import_export',
    'admin_auto_filters',
    
    'django.contrib.humanize',
    'app', # Enable the inner app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"   # Route defined in app/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in app/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "core/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME'  : 'db.sqlite3',
#     }
# }
#testdddd
# DATABASES = {
#     'default': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'Monitoring_VIS',
#         'USER': 'vismonitor',
#         'PASSWORD': 'Thebiggun2524',
#         'HOST': 'WIN-HURQ95SLF1H\SQLEXPRESS',
#         'PORT': '',

#         'OPTIONS': {
#             'driver': 'ODBC Driver 11 for SQL Server',
#         },
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'Monitoring_VIS',
        'USER': 'vismonitor',
        'PASSWORD': 'Thebiggun2524',
        'HOST': '119.59.112.130,1433',
        'PORT': '',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}


# On widows use ODBC 13  xxxxxxxxxxxxxx
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = False

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'core/static'),
)
LINE_CHANNEL_ACCESS_TOKEN = "HiIGJRtQdpcaurQLUKse53RGjSxXrPor0Tx/kLCT26cXid0YH5LKPVpQvLnGXEFqW9Icxn4LsMFylcIePtchAG3b+yHqdmkc31CxUR6B2s9OEfziCXLtKk2U5LzsJdvyJ8AHIoAwGZ0RptLoMWw8/wdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "1f3161681bb10c5a06350426f00c9c73"
FIRST_MENU = 'richmenu-8db65e242d9c0b74d5dbc90f00aa1151'
SECOND_LEVEL = 'richmenu-fc2463365441199552545387f8ca8837'
FIRST_LEVEL = 'richmenu-1cf04547d98b191d2367af60c9d623c4'
# DEFULT_RICH_MENU ="richmenu-a1266a264e8ad9fe600132eef3200825"
# CBRE_MENU = "richmenu-098c9ee37d0eee2e2ff123ef8799c928"
# CONTRACTOR_MENU = "richmenu-5f9022a3f1aa905d8a6860dd87f3414f"
#############################################################
#############################################################
now = timezone.now()
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print(now)
print (today)