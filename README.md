# Chipy.org

This is the code for the Chipy.org website.
This project is open source, and the license can be found in LICENSE.

[![CircleCI](https://circleci.com/gh/chicagopython/chipy.org/tree/master.svg?style=svg)](https://circleci.com/gh/chicagopython/chipy.org/tree/master)

Chipy.org uses the [12factor](http://12factor.net) methodology. The site is
normally powered by Heroku, but you can use Docker and Docker Compose for
local development.

## Installation

To get setup with chipy.org code, it is recommended that you use the following:

For Mac and Linux:
* Docker - https://docs.docker.com/install/
* Docker Compose - https://docs.docker.com/compose/install/
* Make - https://www.gnu.org/software/make/

For Windows 10 Pro, 64-bit:
* Docker - https://docs.docker.com/install/
* Docker Compose - https://docs.docker.com/compose/install/
* Chocolatey - https://chocolatey.org/install (package manager used to install Make)

For Windows 7 to 10 Non Pro, 64-bit:
* Docker Toolbox - https://docs.docker.com/toolbox/toolbox_install_windows/
* Chocolatey - https://chocolatey.org/install (package manager used to install Make)

### Instructions for Windows 7 to 10 Users (Non Pro)

For Windows 7 to 10 users not using Windows 10 Pro, we recommend using Docker Toolbox. Use the package manager Chocolatey to install Make. (See instructions in the section below for that.) Then click on `Docker Quickstart` on your Desktop to get the Docker Toolbox terminal. Using the Docker Toolbox terminal, follow the "Setting up a Local Development Environment Using Docker" instructions below. Once you have the database and web app up, select the `default` virtual machine in VirtualBox. Set up NAT port forwarding, where the Guest Port is 8000 and the Host Port is 8000. Guest IP and Host IP are left empty. Go to `localhost:8000` on your browser to see the site.

Note: A `.gitattributes` file has been provided to keep line endings as LF, instead of CRLF, on checkout and commit. Issues related to developing on Windows with Docker Toolbox are likely related to files having incorrect line endings.

### Using Chocolatey to install Make

For Windows users, we recommend using the package manager Chocolatey to install Make.

1. Install Chocolatey from https://chocolatey.org/install . Open Powershell as administrator when following the instructions.

2. Once Chocolatey is installed, run the following command in Powershell (as administrator):

    `choco install make`

## Setting up a Local Development Environment using Docker

Sign into your GitHub account. Make a fork of the ChiPy repo at https://github.com/chicagopython/chipy.org by going there and clicking "Fork" on the upper right corner.

Clone this forked repo to your local computer (replace your GitHub username without the brackets): 

    git clone https://github.com/<your-GitHub-username>/chipy.org.git chipy.org

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

You can confirm that the migrations were successful. To do this, run `make shell` , which gives you a Bash shell within Docker. Then run `python manage.py migrate --list` . This shows a list of all the migrations. Make sure each migration has a marked checkbox, such as `[X] 0001_initial` . Then exit out of the shell by typing `exit` .

Next, you should create a superuser to use to login to the site admin with.

    make super

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

Chipy.org uses Black to have consistently formatted code. We also use isort to 
arrange import statements correctly. Code must be formatted before merging code.
If you would like to format code, run the following:

    make format

Note: the command `make format` overwrites your files. To see a preview of what formatted code would 
look without overwriting your files, run the following:

    make format-check

If you want to execute a shell into your container, run the following:
once your app is running with `make up`:

    make shell

If you want to see the application logs, use the following command. To stop
viewing the logs, you can press ctl-c.

    make log

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

This repo uses date-based tagging as it is not a library (normally semver). To
create a new tag run `make tag`. Tags should be created at every deploy.

### Heroku Testing

It is recommended that you deploy to a personal Heroku account to test, but
regardless you can deploy a feature branch with the following command:

    # Deploy feature branch
    git push heroku feature/mybranch:master
