"""
ASGI config for backendDrewdru project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backendDrewdru.settings")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(f"{BASE_DIR}/.env.prod", "a+") as f:
    os.environ.update(line.strip().split("=", 1) for line in f)

application = get_asgi_application()
