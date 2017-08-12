# Debian based image
FROM ubuntu:16.04
# reduce image size by cleaning up after install
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libjpeg-dev \
    libfreetype6 \
    libfreetype6-dev \
    libpq-dev \
    postgresql-client \
    python3-dev \
    python3-venv \
    zlib1g-dev \
    ruby-sass \
    libpcre3 libpcre3-dev \
    && rm -rf /var/lib/apt/lists/*

# set the environment variable default; can be overridden by compose
ENV SITE_DIR=/site/
ENV PROJECT_NAME="chipy_org"
RUN mkdir -p $SITE_DIR
WORKDIR $SITE_DIR
RUN mkdir -p proj/ var/log/ htdocs/

# create a virtualenv to separate app packages from system packages
RUN python3 -mvenv env/
#COPY docker-utils/ssl/ ssl/

# pre-install requirements; doing this sooner prevents unnecessary layer-building
COPY requirements.txt requirements.txt
RUN env/bin/pip install pip --upgrade
RUN env/bin/pip install -r requirements.txt

# Make sure that we install uwsgi, regardless of project requirements
RUN env/bin/pip install uwsgi

# Set some environment variables; can be overridden by compose
ENV NUM_THREADS=2
ENV NUM_PROCS=2
ENV DJANGO_DATABASE_URL=postgres://postgres@db/postgres
ENV ADMINS=""
ENV ENVELOPE_EMAIL_RECIPIENTS=""
ENV SECRET_KEY="set-this-to-something-random-and-sercure-in-production"

# Copy in docker scripts
COPY docker-utils/ docker-utils/

# Copy in project files
COPY . proj/

EXPOSE 8000

# Set a custom entrypoint to let us provide custom initialization behavior
ENTRYPOINT ["./docker-utils/entrypoint.sh"]

# Set the command to start uwsgi
CMD ["./docker-utils/app-start.sh"]
