#!/bin/bash
echo "--- INTENTO DEFINITIVO: LIMPIEZA QUIRÚRGICA ---"

# 1. Limpiamos datos viejos
python manage.py flush --noinput

# 2. Creamos las tablas (aquí es donde se pueden crear perfiles vacíos)
python manage.py migrate --noinput

# 3. BORRAMOS LOS PERFILES AUTOMÁTICOS (Este es el secreto)
# Esto limpia la tabla de perfiles para que el JSON no choque
python manage.py shell -c "from perfiles.models import Perfil; Perfil.objects.all().delete(); print('Tablas de perfiles despejadas')"

# 4. Ahora cargamos tus datos
python manage.py loaddata datadump.json

# 5. Finalizamos
python manage.py collectstatic --noinput
gunicorn MONSTER_APP.wsgi --bind 0.0.0.0:$PORT