#!/bin/bash
echo "Iniciando limpieza profunda..."

# 1. Forzar la limpieza de datos existentes
python manage.py flush --noinput

# 2. Asegurar que las tablas estén sincronizadas
python manage.py migrate --noinput

# 3. TRUCO: Borrar el registro que causa el choque antes de cargar el JSON
# Esto elimina específicamente el perfil que bloquea al usuario 2
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('TRUNCATE TABLE perfiles_perfil CASCADE;')"

# 4. Ahora sí, cargar tus datos
python manage.py loaddata datadump.json

# 5. Archivos estáticos y arranque
python manage.py collectstatic --noinput
gunicorn MONSTER_APP.wsgi --bind 0.0.0.0:$PORT