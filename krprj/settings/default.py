# Django settings for krprj project.
import os

# Celery
import djcelery
djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Kirchenreich Team', 'team@kirchenreich.org'),
)

MANAGERS = ADMINS

if False:
    # template to copy in local_settings.py and fill.
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'kirchenreich',
            # 'USER': '',
            # 'PASSWORD': '',
            }
        }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

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
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
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
    'compressor.finders.CompressorFinder'
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = None

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'krprj.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'krprj.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates")
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'django.contrib.humanize',
    'south',
    'djcelery',
    'compressor',
    'compressor_celery',
#    'djangosecure',

    'krprj.krunite',
    'krprj.osm',
    'krprj.wikipedia',
    'krprj.world',
    'krprj.worshipmap',
    'krprj.api',
]

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

# More celery
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Setting X-Frame-Options for all responses
X_FRAME_OPTIONS = 'DENY'

# django-secure
#SESSION_COOKIE_SECURE = True
#SECURE_HSTS_SECONDS = 1
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_FRAME_DENY = True
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True
#SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

ALLOWED_HOSTS = ('.kirchenreich.org', '141.58.160.16', '/fs/web/kirchenreich/var/run/gunicorn.sock:80', '127.0.0.1')
