#!/usr/bin/env bash
. ./export_env.sh
cd xnote
python manage.py makemigrations
python manage.py migrate
python manage.py runserver