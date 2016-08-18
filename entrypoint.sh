#!/bin/bash

set -e

sleep 5

case "$1" in
    web)
        (cd ..; alembic upgrade head)
        python -m gitmostwanted.web
        ;;

    celery)
        celery --app=gitmostwanted.app.celery purge --force
        rm -f /tmp/{celery.pid,celerybeat-schedule.dat,celerybeat-schedule.dir}
        celery worker --app=gitmostwanted.app.celery --beat \
            --events --loglevel=DEBUG --pidfile=/tmp/celery.pid \
            --schedule=/tmp/celerybeat-schedule
        ;;

    *)
        echo $"Usage: $0 {web|celery}"
        exit 1
esac
