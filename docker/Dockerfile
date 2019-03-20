FROM python:2.7.15

# install os dependencies; clean apt cache
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libjpeg-dev \
    libfreetype6 \
    libfreetype6-dev \
    zlib1g-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# environment variables needed 
ENV SITE_DIR=/site/
ENV PYTHONPATH="${SITE_DIR}proj/"
ENV PATH="${PATH}:/home/app/.local/bin/"
ENV NUM_THREADS=2
ENV NUM_PROCS=2

# Create new application user
RUN groupadd -r app && \
    useradd -r -g app -d /home/app -c "Docker image user" app

# Create user dirs, set perms on user dirs and switch to user
RUN install -g app -o app -d ${SITE_DIR}
WORKDIR ${SITE_DIR}
RUN install -g app -o app -d proj/ var/log/ htdocs/ htdocs/static/ /home/app
RUN find ${SITE_DIR} -type d -exec chmod g+s {} \;
RUN chmod -R g+w ${SITE_DIR}
USER app

# Install python packages
ADD requirements.txt ${SITE_DIR}requirements.txt
ADD requirements_test.txt ${SITE_DIR}requirements_test.txt
RUN pip install --user -r ${SITE_DIR}requirements_test.txt
RUN pip install --user uwsgi
COPY docker/ ${SITE_DIR}docker/
ADD . proj/

WORKDIR ./proj/
EXPOSE 8000

ENTRYPOINT ["./docker/entrypoint.sh"]
CMD ["./docker/app-start.sh"]
