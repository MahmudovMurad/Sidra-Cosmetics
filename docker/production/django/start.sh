#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

uv run python manage.py makemigrations --no-input
uv run python manage.py migrate --no-input
uv run python manage.py collectstatic --no-input
exec uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 60