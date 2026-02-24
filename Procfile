release: python manage.py migrate
web: gunicorn MONSTER_APP.wsgi --bind 0.0.0.0:$PORT