from __future__ import absolute_import
import os
import sys

import django
from celery import Celery
from django.conf import settings

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backendDrewdru.settings_prod")

settings_file = "backendDrewdru.settings_dev"
if "prod" in sys.argv:
    settings_file = "backendDrewdru.settings_prod"
#     sys.argv.remove("prod")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)



django.setup()
# celery worker -A backendDrewdru -l debug
app = Celery("backendDrewdru")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# celery -A testapp beat -l debug
# from celery.schedules import crontab
# app.conf.beat_schedule = {
#     'run-every-single-minute': {
#         'task': 'testapp.tasks.hello_world',
#         'schedule': crontab(),
#     },
# }
