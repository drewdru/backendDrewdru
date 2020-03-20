import os

from .settings import *

env_file_path = f"{BASE_DIR}/.env"
if os.path.exists(env_file_path):
    environ.Env.read_env(env_file_path)

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

# region DebugToolbar
MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS.append("debug_toolbar")
INTERNAL_IPS = ("127.0.0.1", "localhost")
# endregion

# region Database
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "ENFORCE_SCHEMA": False,
        "LOGGING": {
            "version": 1,
            "loggers": {"djongo": {"level": "DEBUG", "propogate": False,}},
        },
        "NAME": env("MONGO_DB_NAME"),
        "CLIENT": {
            "host": env("MONGO_DB_HOST"),
            "port": env("MONGO_DB_PORT"),
            "username": env("MONGO_DB_USER"),
            "password": env("MONGO_DB_PASSWORD"),
            "authSource": env("MONGO_DB_AUTH_SOURCE"),
        },
    }
}
# endregion
