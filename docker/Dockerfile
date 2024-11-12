FROM python:3.11.10

# install os dependencies; clean apt cache
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libz-dev\
    libjpeg-dev \
    libfreetype6 \
    libfreetype6-dev \
    zlib1g-dev \
    libpq-dev \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# environment variables needed
ENV SITE_DIR=/site/
ENV PYTHONPATH="${SITE_DIR}proj/"
ENV NUM_THREADS=2
ENV NUM_PROCS=2

WORKDIR ${SITE_DIR}
RUN install -d proj/ var/log/ htdocs/ htdocs/static/

# Install python packages
ADD pyproject.toml ${SITE_DIR}pyproject.toml
RUN pip install -e .[dev]
RUN pip install uwsgi

COPY docker/ ${SITE_DIR}docker/
ADD . proj/

WORKDIR ./proj/
EXPOSE 8000

ENTRYPOINT ["./docker/entrypoint.sh"]
CMD ["./docker/app-start.sh"]
