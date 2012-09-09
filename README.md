=========
Chipy.org
=========

The code for the Chipy.org website
This project is open source and the license can be found in LICENSE.


Installation
============

To get setup with chipy.org code it is recommended that you use the following:

 * Python 2.6+
 * virtualenv
 * [Autoenv](https://github.com/kennethreitz/autoenv)
 * C compiler (for PIL)

Setting up environment
----------------------

Chipy.org is setup using [12factor](http://12factor.net), which means that it takes local settings from the environment. For this reason it is recommended that you use autoenv and a .env file. The example .env is::

    export DEBUG=True
    export GITHUB_APP_ID=youridhere
    export GITHUB_API_SECRET=supersecretkeyhere

If using autoenv, the above will be in your environment when you cd to the project directory

Create a virtual environment where your dependencies will live::

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$

Clone the repo

    (venv)$ git clone git://github.com/chicagopython/chipy.org.git chipy.org

Make the project directory your working directory::

    (venv)$ cd chipy.org

Install project dependencies::

    (venv)$ pip install -r requirements.txt

Setting up the database
-----------------------

This will vary for production and development. By default the project is set
up to run on a SQLite database. If you are setting up a production database
see the Configuration section below for where to place settings and get the
database running. Now you can run::

    (venv)$ python manage.py syncdb

Running a web server
--------------------

In development you should run::

    (venv)$ python manage.py runserver


