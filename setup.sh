#!/bin/bash
echo "--- DESPLIEGUE EN BASE DE DATOS LIMPIA ---"

# 1. Crear las tablas desde cero
python manage.py migrate --noinput

# 2. CARGAR TUS DATOS (Ahora no habrá choques)
python manage.py loaddata datadump.json

# 3. Archivos estáticos y encendido
python manage.py collectstatic --noinput
gunicorn MONSTER_APP.wsgi --bind 0.0.0.0:$PORT