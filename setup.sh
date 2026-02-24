#!/bin/bash
# 1. Crear las tablas en la base de datos limpia
python manage.py migrate --noinput

# 2. Cargar tus datos (Ahora entrarán sin errores de duplicidad)
python manage.py loaddata datadump.json

# 3. Preparar archivos estáticos
python manage.py collectstatic --noinput

# 4. Arrancar la web
gunicorn MONSTER_APP.wsgi --bind 0.0.0.0:$PORT