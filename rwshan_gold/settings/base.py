"""
Base settings for rwshan_gold project.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'debug_toolbar',
    
    # Third-party apps
    'jazzmin',  # Admin theme
    'parler',  # For translations
    
    # Local apps
    # 'core.apps.CoreConfig',
    # 'products.apps.ProductsConfig',
    # 'configurator.apps.ConfiguratorConfig',
    # 'quotes.apps.QuotesConfig',
    # 'blog.apps.BlogConfig',
    # 'testimonials.apps.TestimonialsConfig',
    # 'contact.apps.ContactConfig',
     
    'blog',
    'configurator',
    'contact',
    'core',
    'products',
    'quotes',
    'testimonials',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'rwshan_gold.urls'

# Redirects after login/logout
LOGIN_REDIRECT_URL = '/quotes/list/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# The URL for login page (default is /accounts/login/)
LOGIN_URL = '/accounts/login/'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # For i18n
            ],
        },
    },
]

WSGI_APPLICATION = 'rwshan_gold.wsgi.application'

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'rwshan_gold_db'),
#         'USER': os.environ.get('DB_USER', 'rwshan_gold_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # تأكد من المسار حسب موقع الملف

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ar'  # Arabic as primary
LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_T10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

HUGGINGFACE_API_TOKEN  = "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"
# HUGGINGFACE_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN', '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')
# HUGGINGFACE_API_TOKEN = config('HUGGINGFACE_API_TOKEN', default='')
# DEBUG = config('DEBUG', default=False, cast=bool)


MEDIA_ROOT = Path(BASE_DIR) / "media"
MEDIA_URL = "/media/"
# Media files
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site ID for Django sites framework
SITE_ID = 1

# Django Parler settings
PARLER_LANGUAGES = {
    1: (
        {'code': 'ar',},  # Arabic
        {'code': 'en',},  # English
    ),
    'default': {
        'fallback': 'ar',  # Fallback to Arabic if translation not available
        'hide_untranslated': False,
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}