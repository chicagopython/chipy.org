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
    export SECRET_KEY=somesecretkeyfordjangogoeshere
    export ADMINS=admin@example.com
    export ENVELOPE_EMAIL_RECIPIENTS=admin@example.com

Note that the only required config is the github stuff. The secret key will be random by default which will cause your session to wipe on every restart.

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

I recommend keeping your development DB as close to production as possible. If you're on a Mac, I recommend using [Postgress.app](http://postgresapp.com)

You will need to run::

    (venv)$ python manage.py syncdb

Running a web server
--------------------

In development you should run::

    (venv)$ python manage.py runserver
