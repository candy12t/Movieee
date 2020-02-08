from .settings_common import *


DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'
