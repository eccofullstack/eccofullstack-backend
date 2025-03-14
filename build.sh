#!/usr/bin/env bash
# exit on error
set -o errexit

# Cargar variables de entorno desde .env
export $(grep -v '^#' .env | xargs)

# Instalar dependencias
pip install -r requirements.txt

python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario automáticamente si no existe
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Superusuario creado con éxito")
else:
    print("⚠️ El superusuario ya existe o faltan datos")
EOF
