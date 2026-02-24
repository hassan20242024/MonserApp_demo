#!/bin/bash
python manage.py flush --noinput
python manage.py loaddata datadump.json
python manage.py collectstatic --noinput
gunicorn MONSTER_APP.wsgi --bind 0.0.0.0:$PORT