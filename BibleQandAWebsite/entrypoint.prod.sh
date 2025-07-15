#!/usr/bin/env bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn server..."
exec gunicorn bibleqna.wsgi:application --bind 0.0.0.0:8000 --workers 3

