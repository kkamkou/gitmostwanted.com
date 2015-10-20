#!/bin/bash
set -e

case "$1" in
    web)
        (cd ..; alembic upgrade head)
        python -m gitmostwanted.web
        ;;

    celery)
        rm -f /tmp/celerybeat-schedule.dat
        celery -A gitmostwanted.app.celery worker -B -s /tmp/celerybeat-schedule.dat --autoreload --loglevel=DEBUG
        ;;

    *)
        echo $"Usage: $0 {web|celery}"
        exit 1
esac
