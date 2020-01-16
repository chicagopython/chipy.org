# Chipy.org

The code for the Chipy.org website
This project is open source and the license can be found in LICENSE.

[![CircleCI](https://circleci.com/gh/chicagopython/chipy.org/tree/master.svg?style=svg)](https://circleci.com/gh/chicagopython/chipy.org/tree/master)

Chipy.org is setup using the [12factor](http://12factor.net) methodology. The site is
normally powered by Heroku, but you can use Docker and Docker Compose for
local development.

## Installation

To get setup with chipy.org code it is recommended that you use the following:

* Docker - https://docs.docker.com/install/
* docker-compose - https://docs.docker.com/compose/install/
* make - https://www.gnu.org/software/make/

## Setting up a Local development environment using Docker

Clone the repo

    git clone git://github.com/chicagopython/chipy.org.git chipy.org

Make the project directory your working directory:

    cd chipy.org

Run the setup command to configure the environment. This will copy
a default configuration file from docker/docker.env.sample to
docker/docker.env.

    make setup_env

You may customize the docker/docker.env as needed for your development needs.  
The docker/docker.env file should NOT be committed version control.

To start the app, you can run the following command.  This will start
up the web app and a database as services using docker-compose.

    make up

After running `make up`, you need to migrate the database. This will
create the tables and database objects needed to run the site. 

Note: After running `make migrate` the first time, an error message may appear. If the error message looks like `psycopg2.ProgrammingError: relation "django_site" does not exist`, you can ignore it. Run `make migrate` a second time. This error message should now be gone. 

If after running `make migrate` the first time you get a different error message than the one above, run `make migrate` again. If the error message still appears, you should troubleshoot it.

    make migrate

Next, you should create a superuser to use to login to the site admin with.

    docker-compose exec web ./manage.py createsuperuser

Finally, you should be able to visit your site by entering the
following in your url bar:

    http://localhost:8000

For local development, Social Auth will be disabled by default. Therefore,
to log into the Django Admin interface, you will need to visit the following
url and login with the superuser credentials that you created above.

     http://localhost:8000/admin/

Chipy.org uses Pytest to help ensure code is working properly.
All tests must pass before merging code, and tests should be added as
new functionality is added.
If you would like to run tests for the app, run the following:

    make test

Chipy.org uses Pylint to encourage good software development techniques.
All Pylint checks must pass before merging code.
If you would like to run the Pylint linting process, run the following:

    make lint

If you want to execute a shell into your container, run the following:
once your app is running with `make up`:

    docker-compose exec web bash

If you want to see the application logs, use the following command. To stop
viewing the logs, you can press ctl-c.

    docker-compose logs -f web

To run an arbitrary Django management command, you can use the following form.
The below example shows you how to run the `help` management command, but
other Django management commands can be run the same way.

    docker-compose exec web ./manage.py help

## Heroku Commands

This application is deployed to production using Heroku. You should not need
to use these for basic site development, but are provided here as a guide for
people deploying the site to Heroku.

    # Tag the release
    git tag -m x.x.x x.x.x
    git push --tags

    # Deploy changes to master
    git push heroku master

    # Collectstatic
    heroku run python manage.py collectstatic --noinput

    # Set sync and migrate the database
    heroku run python manage.py migrate

    # Set environment variable on Heroku
    heroku config:set DEBUG=False

### Tagging

ChiPy follows loose [Semantic Versioning](https://semver.org/) rules. Almost
every deploy will be a minor version except where a significant UI or API
change happens or a change likely breaks many feature branches.

### Heroku Testing

It is recommended that you deploy to a personal Heroku account to test, but
regardless you can deploy a feature branch with the following command:

    # Deploy feature branch
    git push heroku feature/mybranch:master
