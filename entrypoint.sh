#!/bin/bash
set -e

(cd ..; alembic upgrade head)

python -m gitmostwanted.web
