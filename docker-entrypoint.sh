#!/bin/bash

echo "Make migrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

echo "Seed database"
python manage.py loaddata boilerplate/database/seed.json

echo "Starting server"
gunicorn --bind 0.0.0.0:80 --access-logfile - boilerplate.wsgi
