"""
Django settings for store project.
Production-Ready Configuration.
"""
import os
from pathlib import Path
import dj_database_url  # NEW LIBRARY

from django.contrib.messages import constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY CONFIGURATION ---

# Reads the secret key from the environment or uses an insecure one for local dev only
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-me')

# In production, DEBUG must be False.
# Here we say: If the DEBUG variable doesn't exist, assume False.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Reads allowed hosts from the environment (e.g., 'mysite.railway.app,other.com')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# To avoid CSRF errors in admin when hosted on HTTPS (Railway/Render)
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.vercel.app']


# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'products',
    'orders',
    'profiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Must be before whitenoise
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_TEMPLATE_PACK = 'bootstrap5'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ADDED: Serves static files in production
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'store.wsgi.application'


# --- DATABASE CONFIGURATION ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# The magic happens here:
# If DATABASE_URL exists (Railway), use Postgres.
# If it doesn't exist (local PC), use local SQLite.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# --- PASSWORD VALIDATION ---

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


# --- INTERNATIONALIZATION ---

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES (CSS, JavaScript, Images) ---

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# WhiteNoise configuration to compress and cache files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- MEDIA FILES ---
# Note: On free hosting (Railway/Vercel/Render), media files
# (user uploads) are deleted on every deploy.
# For real persistence, AWS S3 or Cloudinary is required.

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


MESSAGE_TAGS = {
    constants.DEBUG: 'alert-info',
    constants.ERROR: 'alert-danger',
    constants.INFO: 'alert-info',
    constants.SUCCESS: 'alert-success',
    constants.WARNING: 'alert-warning',
}

# Session settings: 7 days
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
SESSION_SAVE_EVERY_REQUEST = False
