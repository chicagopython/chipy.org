=========
Getting Started with Docker for Local Development:
============

To get setup with chipy.org code using Docker it is recommended that you use the following:

 * Docker
 * virtualenv

Setting up a Local environment
------------------------------

Create a virtual environment where your dependencies will live::

    $ virtualenv venv
    $ source venv/bin/activate

Clone the repo

    git clone git://github.com/chicagopython/chipy.org.git chipy.org

Make the project directory your working directory::

    cd chipy.org

Install project dependencies::

    pip install -r requirements.txt

Start [a docker instance for Postgres](https://hub.docker.com/_/postgres/):

    docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres

Connect to the instance and set up a `chipy` database:

    docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -U postgres
     > create database chipy;

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

Note that the only required config is the github stuff. The secret key will be random by default which will cause your session to wipe on every restart.


Migrate the database to build your :

    # first time (this command notoriously throws errors, don't panic)
    python manage.py migrate auth

    # after future migrations
    python manage.py makemigrations
    python manage.py makemigrations

Now you can run the server!

    (venv)$ python manage.py runserver

Happy Dev'ing!
