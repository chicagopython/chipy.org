Getting Started with Docker for Local Development
============

To get setup with chipy.org code using Docker it is recommended that you use the following:

 * Docker = https://docs.docker.com/engine/installation/#cloud
 * Docker Compose = https://docs.docker.com/compose/install/

Setting up a Local environment
------------------------------

Clone the repo

    git clone git://github.com/chicagopython/chipy.org.git chipy.org

Make the project directory your working directory:

    cd chipy.org

Build the environment:

    docker-compose up --build


Initialize the application (migrate):

    docker-compose run app init

Create a superuser:

    docker-compose run app manage createsuperuser

Open a browser:

    http://localhost:8000/


Other Docker Commands:
------------------------------

Run a bash shell (automatically activates virtualenv):

    docker-compose run app /bin/bash

Shortcut to run Management Command:

    docker-compose run app manage help


Create an env file in the root directory:

    export DEBUG=True
    export ALLOWED_HOSTS="chipy.org,www.chipy.org"
    export GITHUB_APP_ID=youridhere
    export GITHUB_API_SECRET=supersecretkeyhere
    export SECRET_KEY=somesecretkeyfordjangogoeshere
    export ADMINS=admin@example.com
    export ENVELOPE_EMAIL_RECIPIENTS=admin@example.com
    export NORECAPTCHA_SITE_KEY=your_recaptcha_public_key
    export NORECAPTCHA_SECRET_KEY=your_recaptcha_private_key
    export DATABASE_URL=postgres://postgres:mysecretpassword@localhost:5432/chipy

    # settings needed for social authentication
    export GITHUB_API_SECRET=""
    export GITHUB_APP_ID=""
    export GOOGLE_OAUTH2_CLIENT_ID=""
    export GOOGLE_OAUTH2_CLIENT_SECRET=""

    # optional email settings and their defaults
    export EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    export EMAIL_HOST='smtp.sendgrid.net'
    export EMAIL_PORT=587
    export EMAIL_USE_TLS=True
    export EMAIL_HOST_USER=""
    export EMAIL_HOST_PASSWORD=""

    # to enable S3, do the following
    export USE_S3="True"
    export AWS_ACCESS_KEY_ID=""
    export AWS_SECRET_ACCESS_KEY=""
    export AWS_STORAGE_BUCKET_NAME=""

Source your env:

    source .env
