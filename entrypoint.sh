#!/bin/bash

set -e

sleep 5

case "$1" in
    web)
        alembic upgrade head
        python -m gitmostwanted.web
        ;;

    celery)
        [[ "${GMW_APP_ENV}" -ne "production" ]] \
            && celery --app=gitmostwanted.app.celery purge --force || true
        rm -f /tmp/celery.pid
        celery worker --app=gitmostwanted.app.celery --beat \
            --events --loglevel=INFO --pidfile=/tmp/celery.pid \
            --schedule=/data/celerybeat-schedule --logfile=/data/celery.log
        ;;

    *)
        echo $"Usage: $0 {web|celery}"
        exit 1
esac
