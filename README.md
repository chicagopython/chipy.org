=========
Chipy.org
=========

This repository stores the Pinax Symposion conference starter project. 
This project is open source and the license can be found in LICENSE.


Installation
============

To get setup with chipy.org code you must have the following
installed:

 * Python 2.6+
 * virtualenv 1.4.7+
 * C compiler (for PIL)

Setting up environment
----------------------

Create a virtual environment where your dependencies will live::

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$

Clone the repo

    (venv)$ git clone git://github.com/chicagopython/chipy.org.git chipy.org

Make the project directory your working directory::

    (venv)$ cd chipy.org

Install project dependencies::

    (venv)$ pip install -r requirements/project.txt

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

For production, this project comes with a WSGI entry point located in
``deploy/wsgi.py`` and can be referenced by gunicorn with
``deploy.wsgi:application``.

Configuration
=============

You can create a ``local_settings.py`` file alongside ``settings.py`` to
override any setting that may be environment/instance specific. This file is
ignored in ``.gitignore``.
