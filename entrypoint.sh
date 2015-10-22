#!/bin/bash
set -e

case "$1" in
    web)
        (cd ..; alembic upgrade head)
        python -m gitmostwanted.web
        ;;

    celery)
        rm -f /tmp/celerybeat-schedule.dat
        celery --app=gitmostwanted.app.celery worker --beat --detach \
            --events --logfile=celery.log --loglevel=DEBUG \
            --pidfile=celery.pid --schedule=/tmp/celerybeat-schedule.dat
        ;;

    *)
        echo $"Usage: $0 {web|celery}"
        exit 1
esac
