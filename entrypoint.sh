#!/bin/sh

set -e

sleep 5

case "$1" in
    web)
        alembic upgrade head
        python -m gitmostwanted.web
        ;;

    celery)
        ([ "${GMW_APP_ENV}" != "production" ] && celery --app=gitmostwanted.app.celery purge --force) || true
        rm -f /tmp/celery.pid

        DIR_DATA=`[ -w "/data" ] && echo "/data" || echo "/tmp"`
        echo "Data folder: ${DIR_DATA}"

        celery --app=gitmostwanted.app.celery worker --beat \
            --events --loglevel=INFO --pidfile=/tmp/celery.pid \
            --schedule="${DIR_DATA}/celerybeat-schedule" --logfile="${DIR_DATA}/celery.log"
        ;;

    *)
        echo "Usage: ${0} {web|celery}"
        exit 1
esac
