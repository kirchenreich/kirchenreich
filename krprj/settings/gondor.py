import os
import urlparse

from .default import *

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.contrib.gis.db.backends.postgis"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

if 'SECRET_KEY' in os.environ:
   SECRET_KEY = os.environ['SECRET_KEY']

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "media")
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "static")

MEDIA_URL = '/media/'
STATIC_ROOT = '/static/'
