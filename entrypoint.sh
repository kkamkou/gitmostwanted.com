#!/bin/sh

set -e

python - <<'EOF'
import sys, time
from sqlalchemy import create_engine
from gitmostwanted.app import app

uri = app.config.get('SQLALCHEMY_DATABASE_URI')
if uri and not uri.startswith('sqlite'):
    engine = create_engine(uri)
    for _ in range(30):
        try:
            with engine.connect():
                break
        except Exception:
            time.sleep(1)
    else:
        sys.exit(1)
EOF

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
