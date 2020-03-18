from .settings import *

DEBUG = True

# region CORS
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ["http://localhost", "http://127.0.0.1"]
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http://127.0.0.1:\d+$",
    r"^http://localhost:\d+$",
]
# endregion

# Debug toolbar
MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS.append("debug_toolbar")
INTERNAL_IPS = ("127.0.0.1", "localhost")
