from .settings import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Debug toolbar
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS.append('debug_toolbar')
INTERNAL_IPS = ('127.0.0.1', 'localhost')