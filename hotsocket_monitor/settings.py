# Django settings for hotsocket_monitor project.

import os
import djcelery


djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def abspath(*args):
    """convert relative paths to absolute paths relative to PROJECT_ROOT"""
    return os.path.join(PROJECT_ROOT, *args)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hotsocket_monitor',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = abspath('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = abspath('static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# Leaving this intentionally blank because you have to generate one yourself.
SECRET_KEY = 'please-change-me'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hotsocket_monitor.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hotsocket_monitor.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    abspath('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'gunicorn',
    'django_nose',
    'raven.contrib.django.raven_compat',
    'djcelery',
    'djcelery_email',
    'debug_toolbar',

    # sample apps to explain usage
    'celery_app',
    'monitor',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Celery configuration options
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

CELERY_RESULT_BACKEND = "database"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Uncomment if you're running in DEBUG mode and you want to skip the broker
# and execute tasks immediate instead of deferring them to the queue / workers.
# CELERY_ALWAYS_EAGER = DEBUG

# Tell Celery where to find the tasks
# CELERY_IMPORTS = ('celery_app.tasks',)

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'login-every-24-hours': {
        'task': 'monitor.tasks.run_tasks',
        'schedule': timedelta(seconds=60),
    },
}


# Defer email sending to Celery, except if we're in debug mode,
# then just print the emails to stdout for debugging.
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        # DEBUGGING STUFF
    INTERNAL_IPS = ("http://127.0.0.1")

    # EMAIL
    # In order to debug do python smtp hosting on port 1025
    EMAIL_HOST = "127.0.0.1"
    # EMAIL_HOST_USER = "user"
    # EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 1025
    EMAIL_USER_TLS = True

SENDER = ""
RECIPIENT = ["admin@mail.com", "admin2@mail.com"]

# Django debug toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'ENABLE_STACKTRACES': True,
}

# South configuration variables
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SKIP_SOUTH_TESTS = True     # Do not run the south tests as part of our
                            # test suite.
SOUTH_TESTS_MIGRATE = False  # Do not run the migrations for our tests.
                             # We are assuming that our models.py are correct
                             # for the tests and as such nothing needs to be
                             # migrated.

# Sentry configuration
RAVEN_CONFIG = {
    # DevOps will supply you with this.
    # 'dsn': 'http://public:secret@example.com/1',
}

TESTING = True

# This stores all the settings that will be used in the api

HOTSOCKET_BASE = "http://api.hotsocket.co.za:8080/"

if TESTING:
    HOTSOCKET_RESOURCES = {
        "login": "test/login",
        "recharge": "test/recharge",
        "status": "test/status",
        "statement": "test/statement",
        "balance": "test/balance",
    }

    HOTSOCKET_USERNAME = "trial_acc_1212"
    HOTSOCKET_PASSWORD = "tr14l_l1k3m00n"
else:
    HOTSOCKET_RESOURCES = {
        "login": "login",
        "recharge": "recharge",
        "status": "status",
        "statement": "statement",
        "balance": "balance",
    }

    HOTSOCKET_USERNAME = ""
    HOTSOCKET_PASSWORD = ""

TOKEN_DURATION = 110  # Minutes


HOTSOCKET_CODES = {
    "SUCCESS": {"status": "0000", "message": "Successfully submitted recharge."},
    "TOKEN_INVALID": {"status": 887, "message": "Token is invalid , please login again to obtain a new one."},
    "TOKEN_EXPIRE": {"status": 889, "message": "Token has timed out , please login again to obtain a new one."},
    "MSISDN_NON_NUM": {"status": 6013, "message": "Recipient MSISDN is not numeric."},
    "MSISDN_MALFORMED": {"status": 6014, "message": "Recipient MSISDN is malformed."},
    "PRODUCT_CODE_BAD": {"status": 6011, "message": "Unrecognized product code, valid codes are AIRTIME, DATA, and SMS."},
    "NETWORK_CODE_BAD": {"status": 6012, "message": "Unrecognized network code."},
    "COMBO_BAD": {"status": 6020, "message": " Network code + Product Code + Denomination combination is invalid."},
    "REF_DUPLICATE": {"status": 6016, "message": "Reference must be unique."},
    "REF_NON_NUM": {"status": 6017, "message": "Reference must be a numeric value."},
}

HS_RECHARGE_STATUS_CODES = {
    "PENDING": {"code": 0 },
    "PRE_SUB_ERROR": {"code": 1},
    "FAILED": {"code": 2},
    "SUCCESS": {"code": 3},
}
