from .settings import *

DEBUG = True
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost'
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
)

# Debug toolbar
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS.append('debug_toolbar')
INTERNAL_IPS = ('127.0.0.1', 'localhost')
