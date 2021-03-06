import os
from configparser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

configFilePath = BASE_DIR + "/application.properties"
config = RawConfigParser()
config.read(configFilePath)

SECRET_KEY = config.get('SECURITY', 'SECRET_KEY')
DEBUG = bool(config.get('SECURITY', 'DEBUG'))
SUPERUSER = ['superuser@ipay.com.bd']
ALLOWED_HOSTS = ['*']
TOKEN_LIFE_TIME = int(config.get('SECURITY', 'TOKEN_LIFE_TIME_HOUR')) * 60 * 60
REFRESH_TOKEN_WINDOW = int(config.get('SECURITY', 'REFRESH_TOKEN_WINDOW_SEC'))


# CELERY SETTINGS
CELERY_BROKER_URL = config.get('CELERY', 'CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config.get('CELERY', 'CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = (
    'auth.tasks'
)
# CELERY_TIMEZONE = TIME_ZONE


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'silk',
    'corsheaders',
    'auth_jwt',
    'acl',
    'app',
    'email_domain',
    'group',
    'services',
    'user_group',
    'activity',
    'django_celery_beat',
    'django_celery_results',
]

if DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 10,
    }
else:
    REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'silk.middleware.SilkyMiddleware',
    ]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
    'service-id',
    'app-id',
)

ROOT_URLCONF = 'auth.urls'

WSGI_APPLICATION = 'auth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('DATABASE', 'NAME'),
        'USER': config.get('DATABASE', 'USER'),
        'PASSWORD': config.get('DATABASE', 'PASSWORD'),
        'HOST': config.get('DATABASE', 'HOST'),
        'PORT': config.get('DATABASE', 'PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'development_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/auth.log',
            'when': 'midnight',
            'backupCount': 60,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'acl': {
            'handlers': ['console', 'development_logfile'],
            'level': 'DEBUG',
        },
        'auth_jwt': {
            'handlers': ['console', 'development_logfile'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'development_logfile'],
            'level': 'ERROR',
        },
        'group': {
            'handlers': ['console', 'development_logfile'],
            'level': 'DEBUG',
        },
        'service': {
            'handlers': ['console', 'development_logfile'],
            'level': 'DEBUG',
        },
        'user_group': {
            'handlers': ['console', 'development_logfile'],
            'level': 'DEBUG',
        },
        'activity':{
            'handlers': ['console', 'development_logfile'],
            'level': 'DEBUG',

        }
    }
}


### SILK  ###
SILKY_PYTHON_PROFILER = True

# SILKY_AUTHENTICATION = True  # User must login
# SILKY_AUTHORISATION = True  # User must have permissions
# SILKY_PERMISSIONS = lambda user: user.is_superuser

SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024kb, ignore

SILKY_META = True

if DEBUG:
    SILKY_INTERCEPT_PERCENT = 100 # log only 100% of requests
else:
    SILKY_INTERCEPT_PERCENT = 0 # log only 0% of requests

SILKY_MAX_RECORDED_REQUESTS = 10000
SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10

# python manage.py silk_clear_request_log