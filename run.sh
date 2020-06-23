#!/bin/bash
cd /home/drewdru/develop/python/backendDrewdru/
source env/bin/activate
case $1 in
  dev)
    yes yes | python manage.py collectstatic
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata ./*/fixtures/*.json
    isort -y
	  black . --line-length 80 --exclude './ocr/dataset' --exclude './ocr/fonts' --exclude './ocr/temp'
    # celery worker -A backendDrewdru -n backendDrewdru@drewdru.local &
    python manage.py runserver 8808
    ;;
  prod)
    yes yes | python manage.py collectstatic
    python manage.py migrate
    celery worker -A backendDrewdru -n backendDrewdru@drewdru.com &
    uvicorn backendDrewdru.asgi:application --uds /tmp/backendDrewdru.sock
    ;;
esac
