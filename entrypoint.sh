#!/bin/bash
function db_migration {
    python manage.py makemigrations
    python manage.py migrate
}

function create_admin_user {
    if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
        python manage.py createsuperuser --noinput || true
    fi
}


if [ "$1" = "run" ]; then
    db_migration
    create_admin_user
    exec python manage.py runserver 0.0.0.0:8000
elif [ "$1" = "test" ]; then
    exec python manage.py test
else
    exec "$@"
fi