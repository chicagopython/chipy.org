=========
Getting Started with Docker for Local Development:
============

To get setup with chipy.org code using Docker it is recommended that you use the following:

 * Docker
 * virtualenv

Setting up a Local environment
------------------------------

Clone the repo

    git clone git://github.com/chicagopython/chipy.org.git chipy.org

Make the project directory your working directory::

    cd chipy.org

Run the setup command to configure the environment:

    make setup

Once done, modify the `docker/docker.env` file with the values you require in
your development environment. Reasonable defaults have been provided for local
development.

Then start up your webserver!

    make web

That will start your webserver! If you try to hit the Django app it will throw
an error because you have not yet run migrations. But connectivity is good! And
we can fix migrations with this line in another terminal window:

    make migrate

It works! Right? Try the url in your browser!

    localhost:8000

Once again, that whole package is super easy:

    make setup
    make web
    make migrate

You can run commands like the following to get inside your web server to run any code directly:

    docker exec -it chipy-web bash

Happy Dev'ing!
