"""
Django settings for backendDrewdru project.

Generated by django-admin startproject using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from datetime import timedelta

import environ
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "sz0002i$ktz&3=1c)iq^!$(q46j@a_-#0$5(g3#90o%)_@5mt="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# region CORS
ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "https://drewdru.com",
    "http://localhost",
    "http://127.0.0.1",
]
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.drewdru\.com$",
    r"^http://127.0.0.1:\d+$",
    r"^http://localhost:\d+$",
]
# endregion

# region Install

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "corsheaders",
    "home",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backendDrewdru.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates",],
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

WSGI_APPLICATION = "backendDrewdru.wsgi.application"
# endregion

# region PasswordValidation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# endregion

# region Internationalization
LANGUAGE_CODE = "en-us"
LANGUAGES = (
    ("ru", _("Russian")),
    ("en", _("English")),
)
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
TIME_ZONE = "Asia/Krasnoyarsk"
USE_I18N = True
USE_L10N = True
USE_TZ = True
# endregion

# region static_and_media
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
# endregion

# region GRAPHQL
GRAPHENE = {
    "SCHEMA": "backendDrewdru.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware",],
}
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]
GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=60),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    # Unlimited refresh
    # "JWT_REFRESH_EXPIRED_HANDLER": lambda orig_iat, context: False,
    "JWT_ARGUMENT_NAME": "token",
    "JWT_ALLOW_ARGUMENT": True,
}
# endregion


# region Environ
env = environ.Env(
    MONGO_DB_NAME=(str, "DB_NAME"),
    MONGO_DB_HOST=(str, "127.0.0.1"),
    MONGO_DB_PORT=(int, 27017),
    MONGO_DB_USER=(str, "USER_NAME"),
    MONGO_DB_PASSWORD=(str, "PASSWORD"),
    MONGO_DB_AUTH_SOURCE=(str, "admin"),
)
# endregion
