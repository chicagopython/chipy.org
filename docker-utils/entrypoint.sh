#!/bin/bash

set -eox pipefail

cd ${SITE_DIR}proj/
. ${SITE_DIR}env/bin/activate
if [ "$1" == 'init' ]; then
    echo "Run Migrations"
    ${SITE_DIR}env/bin/python ${SITE_DIR}proj/manage.py migrate
    ${SITE_DIR}env/bin/python ${SITE_DIR}proj/manage.py collectstatic --no-input
elif [ "$1" == 'manage' ]; then
    shift
    echo "Manage.py $@"
    ${SITE_DIR}env/bin/python ${SITE_DIR}proj/manage.py $@
else
    source ${SITE_DIR}env/bin/activate
    exec "$@"
fi
