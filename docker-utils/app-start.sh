#!/bin/bash

echo "Starting uWSGI for ${PROJECT_NAME}"

$SITE_DIR/env/bin/honcho -f Procfile -e .env start

# uwsgi --chdir ${SITE_DIR}proj/ \
#     --module=${PROJECT_NAME}.deploy.wsgi:application \
#     --master \
#     --env DJANGO_SETTINGS_MODULE=${PROJECT_NAME}.settings \
#     --vacuum \
#     --max-requests=5000 \
#     --virtualenv ${SITE_DIR}env/ \
#     --http 0.0.0.0:8000 \
#     --processes $NUM_PROCS \
#     --threads $NUM_THREADS \
#     --python-autoreload=1
