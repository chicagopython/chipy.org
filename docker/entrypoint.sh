#!/bin/bash

export SITE_DIR=${SITE_DIR}
export PYTHONPATH="${SITE_DIR}proj/:${PYTHONPATH}"
export PATH="/home/app/.local/bin/:${PATH}"
export SITE_DIR=${SITE_DIR}

cd ${SITE_DIR}proj/

if [ "$1" == 'init' ]; then
    echo "Run Migrations"
    python ${SITE_DIR}proj/manage.py migrate
    python ${SITE_DIR}proj/manage.py collectstatic --noinput
elif [ "$1" == 'manage' ]; then
    shift
    echo "Manage.py $@"
    python ${SITE_DIR}proj/manage.py $@
elif [ "$1" == 'python' ]; then
    shift
    echo "Manage.py $@"
    python ${SITE_DIR}proj/manage.py shell_plus
else
    exec "$@"
fi
