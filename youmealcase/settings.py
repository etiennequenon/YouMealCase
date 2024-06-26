import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'test_key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
]

MIDDLEWARE = [
]

ROOT_URLCONF = 'youmealcase.urls'

WSGI_APPLICATION = 'youmealcase.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True