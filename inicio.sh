#!/usr/bin/env bash

cd gerenciador
python manage.py migrate
python manage.py shell < inicio.py
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000