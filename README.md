# Chipy.org

The code for the Chipy.org website
This project is open source and the license can be found in LICENSE.

## Installation

To get setup with chipy.org code it is recommended that you use the following:

* Docker - https://docs.docker.com/install/
* docker-compose - https://docs.docker.com/compose/install/
* make - https://www.gnu.org/software/make/

## Setting up a Local development environment using Docker

Chipy.org is setup using [12factor](http://12factor.net) philosophies. It is
normally powered by Heroku, but you can use Docker and Docker compose for
local development.

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

    make migrate

Next, you should create a superuser to use to login to the site admin with.

    docker-compose exec web ./manage.py createsuperuser

Finally, you should be able to visit your site, but entering the
following in your url bar:

    http://localhost:8000

If you would like to run tests for the app, run the following:

    make test

If you want to execute a shell into your container, run the following: 
once your app is running with `make up`:

    docker-compose exec web bash

If you want to see the application logs, use the following command. To stop
viewing the logs, you can press ctl-c.

    docker-compose logs -f web

## Heroku Commands

This application is deployed to production using Heroku. You should not need
to use these for basic site development, but are provided here as a guide for
people deploying the site to Heroku.

    # Deploy changes to master
    git push heroku master

    # Deploy feature branch  
    git push heroku feature/mybranch:master

    # Collectstatic
    heroku run python manage.py collectstatic --noinput

    # Set sync and migrate the database
    heroku run python manage.py migrate

    # Set environment variable on Heroku
    heroku config:set DEBUG=True
