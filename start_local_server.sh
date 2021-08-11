#!/usr/bin/env bash
. ./export_env.sh
cd xnote
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver 127.0.0.1:8181