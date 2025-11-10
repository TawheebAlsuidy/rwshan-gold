from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # For production
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development

EMAIL_HOST = 'smtp.gmail.com'  # Or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'alsuidytauheeb@gmail.com'  # بريد الموقع
EMAIL_HOST_PASSWORD = 'uyrs zksr hztr dlbc'
DEFAULT_FROM_EMAIL = 'tomoto@gmail.com'
COMPANY_EMAIL = 'alsuidytauheeb@gmail.com'  # البريد الذي سيتم إرسال العروض إليه


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # أو 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # أسبوع واحد
SESSION_SAVE_EVERY_REQUEST = True


# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'rwshan_gold_dev',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # تأكد من المسار حسب موقع الملف

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Django Debug Toolbar
# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

# MIDDLEWARE = [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
]