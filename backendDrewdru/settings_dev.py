import os

from .settings import *

env_file_path = f"{BASE_DIR}/.env"
if os.path.exists(env_file_path):
    environ.Env.read_env(env_file_path)

DEBUG = True

SECRET_KEY = "sz0002i$ktz&3=1c)iq^!$(q46j@a_-#0$5(g3#90o%)_@5mt="

# cross-domain cookie
SESSION_COOKIE_DOMAIN = ".drewdru.local"
SESSION_COOKIE_NAME = "drewdrulocalcookie"

# region CORS
ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.0.103",
    "localhost",
    "drewdru.local",
    "*.drewdru.local",
    "drewdru.local:8080",
    "*.drewdru.local:8080",
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "http://localhost",
    "http://127.0.0.1",
    "http://192.168.0.103",
    "http://drewdru.local",
    "http://drewdru.local:8080",
]
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http://127.0.0.1:\d+$",
    r"^http://192.168.0.103:\d+$",
    r"^http://localhost:\d+$",
    r"^http://\w+\.drewdru\.local$",
    r"^http://\w+\.drewdru\.local:\d+$",
]
# endregion

# region DebugToolbar
MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS.append("debug_toolbar")
INTERNAL_IPS = (
    "127.0.0.1",
    "192.168.0.103",
    "localhost",
    "drewdru.local",
    "drewdru.local:8080",
)
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


# region Celery
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
BROKER_URL = "redis://127.0.0.1:6379/0"
BROKER_TRANSPORT = "redis"

CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Krasnoyarsk"
CELERY_DEFAULT_RUOTING_KEY = "backendDrewdru@drewdru.local"
# endregion
