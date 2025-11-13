#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

uv run python manage.py makemigrations --no-input
uv run python manage.py migrate --no-input
uv run python manage.py collectstatic --no-input
exec uv run python manage.py runserver 0.0.0.0:8000