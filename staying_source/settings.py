"""
Django settings for staying_source project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path 

# from staying_source.config import DATABASE_NAME, DB_PASSWORD, DB_USERNAME, ENGINE, HOST_NAME, MEDIA_FOLDER, PORT

# Initialise environment variables
# env = environ.Env()
# environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+lto1knn7#db7zf9%u!@@&%7l13-z83#k(wwdf2^^a&6tw!dhq"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
URL="http://127.0.0.1:8000"
ENGINE="django.db.backends.postgresql"
DATABASE_NAME="postgres_private"
DB_USERNAME="postgres"
DB_PASSWORD="postgres"
HOST_NAME="localhost"
PORT=5432
MEDIA_FOLDER="media/"
SITE_ID = 2
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles", 
    "django.contrib.sites", 
    "allauth", 
    "allauth.account", 
    "allauth.socialaccount", 
    "allauth.socialaccount.providers.google",
    "user_1", 
    "channels", 
    "rest_framework",
]

SOCIALACCOUNT_PROVIDERS = {
    "google":{
        "SCOPE":[
            "profile", 
            "email"
        ], 
        "AUTH_PARAMS":{"access_type":"online"}
        
    }
}
# Channels settings
ASGI_APPLICATION = 'staying_source.routing.application'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware", 
    "allauth.account.middleware.AccountMiddleware"
]

ROOT_URLCONF = "staying_source.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates", 
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "staying_source.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": ENGINE,
        "NAME": DATABASE_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": HOST_NAME,
        "PORT": PORT,
    }
}

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_FOLDER)
MEDIA_ROOT_USER_ICON = os.path.join(BASE_DIR, "media/user_icons/")
# Base url to serve media files
MEDIA_URL = "/media/"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend", 
    "allauth.account.auth_backends.AuthenticationBackend"
)
SOCIALACCOUNT_LOGIN_ON_GET=True
LOGIN_REDIRECT_URL = "/" 
LOGOUT_REDIRECT_URL = "/" 