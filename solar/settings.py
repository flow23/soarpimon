"""
Django settings for solar project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c*r)f^%y2yd9%u$oi(p3rsbdu=iv0at_9zj*6j@_m38&@))uwk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'abcdef',
    'graphs',
    'polls',
    'django_crontab',
#    'rrdviewer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'solar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'graphs.globalContextProcessor.graphCategories',
            ],
        },
    },
]

WSGI_APPLICATION = 'solar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/webapp/solar/solar/static'

# Media files
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
MEDIA_URL = '/media/'

# Settings for django-bootstrap3
BOOTSTRAP3 = {
    'set_required': False,
    'error_css_class': 'bootstrap3-error',
    'required_css_class': 'bootstrap3-required',
    'javascript_in_head': True,
}

# Settings for django-crontabs 
CRONJOBS = [
    ('*/1 * * * *', 'solar.cron.SerialPolling', [], {}, '>> /webapp/solar/solar/solar/cron.log')
]
CRONTAB_LOCK_JOBS = True
#CRONJOBS = [
#    ('*/5 * * * *', 'myproject.myapp.cron.other_scheduled_job', ['arg1', 'arg2'], {'verbose': 0}),
#    ('0   4 * * *', 'django.core.management.call_command', ['clearsessions']),
#]
