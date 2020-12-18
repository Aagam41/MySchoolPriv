"""
Django settings for MySchool project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open('D:\Aagam Projects\Python\Django\MySchool\MySchoolSource\MySchool\env.json') as JSONFile:
    environ = json.load(JSONFile)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ['MYSCHOOL_SETTINGS_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(environ['MYSCHOOL_SETTINGS_DEBUG'] == "True")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'StudentPerformancePrediction.apps.StudentperformancepredictionConfig',
    'StudentPerformance.apps.StudentperformanceConfig',
    'StudentFeedback.apps.StudentfeedbackConfig',
    'MySchoolHome.apps.MyschoolhomeConfig',

    'aagam_packages.django.template_tag_extensions.aagam_template_tag_tweaks',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MySchool.urls'

LOGIN_URL = "http://127.0.0.1:8000/login/"
LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', 'aagam_packages/django/templates'],
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

WSGI_APPLICATION = 'MySchool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': str(environ['MYSCHOOL_SETTINGS_DATABASE_NAME']),
        'USER': str(environ['MYSCHOOL_SETTINGS_DATABASE_USER']),
        'PASSWORD': str(environ['MYSCHOOL_SETTINGS_DATABASE_PASSWORD']),
        'HOST': environ['MYSCHOOL_SETTINGS_DATABASE_HOST'],
        'PORT': environ['MYSCHOOL_SETTINGS_DATABASE_PORT'],
    }
}


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

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [f'{BASE_DIR}/static/']
