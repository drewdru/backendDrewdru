#!/bin/bash
cd /home/drewdru/develop/python/backendDrewdru/
source env/bin/activate
case $1 in
  dev)
    export DJANGO_SETTINGS_MODULE=backendDrewdru.settings_dev
    python manage.py loaddata tasks
    python manage.py runserver
    ;;
#  prod)
  prod)
    export DJANGO_SETTINGS_MODULE=backendDrewdru.settings_prod
    yes yes | python manage.py collectstatic
    python manage.py makemigrations
    python manage.py migrate
    uvicorn backendDrewdru.asgi:application --uds /tmp/backendDrewdru.sock
    ;;
esac
