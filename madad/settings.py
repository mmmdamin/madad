"""
Django settings for madad project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p5qc2fos3m(ho7cbz7a9t6f0hj=ugb184&!71ct$@fe!ba4fl^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if os.environ.get('DATABASE_URL'):
    DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {}
if os.environ.get('DATABASE_URL'):
    import dj_database_url

    DATABASES['default'] = dj_database_url.config()
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',
    'ckeditor',

    'base',
    'account',
    'page',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'madad.urls'

WSGI_APPLICATION = 'madad.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

AUTH_USER_MODEL = 'account.Member'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
MANDRILL_API_KEY = ""
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_CONFIGS = {
    'full_ckeditor': {
        'toolbar': 'Full',
        'width' : '500',

    },
    'basic_ckeditor': {
        'toolbar': 'Basic',
        'width' : '500',
    },
}

LOGIN_URL = '/accounts/login'