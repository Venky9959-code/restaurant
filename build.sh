#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Seed menu data (safe to re-run — uses get_or_create internally)
python manage.py seed_menu

# Collect static files (--clear removes stale files from previous deploys)
python manage.py collectstatic --noinput --clear