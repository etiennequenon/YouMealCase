#!/bin/bash

show_help() {
    echo "Usage: $0 [run|test|manual]"
    echo "  run     - Runs yourmealcase API server"
    echo "  test    - Runs yourmealcase API unit tests"
    echo "  manual  - Runs django server with manual arguments in double quotes"
}

function wait_for_db {
    ./wait_for_db.sh
}

function db_migration {
    python manage.py makemigrations
    python manage.py migrate
}

function create_admin_user {
    if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
        python manage.py createsuperuser --noinput || true
    fi
}

function run {
    wait_for_db
    db_migration
    create_admin_user
    exec python manage.py runserver 0.0.0.0:8000
}

function test {
    exec python manage.py test $2
}

function manual {
    exec python manage.py $1
}

if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

case "$1" in
    run)
        run
        ;;
    test)
        test
        ;;
    manual)
        manual "$2"
        ;;
    *)
        echo "Invalid command: $1"
        show_help
        exit 1
        ;;
esac