FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1


RUN apt-get -qq update \
    && apt-get -qq -y install libpq-dev gcc vim \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean \
    && groupadd -r django \
    && useradd -r -g django django


COPY ./docker/production/backend/gunicorn.sh /gunicorn.sh
RUN sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

COPY ./docker/production/backend/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh

#COPY ./docker/production/backend/celery/worker/start.sh /start-celeryworker.sh
#RUN sed -i 's/\r//' /start-celeryworker.sh \
#    && chmod +x /start-celeryworker.sh

#COPY ./docker/production/backend/celery/beat/start.sh /start-celerybeat.sh
#RUN sed -i 's/\r//' /start-celerybeat.sh \
#    && chmod +x /start-celerybeat.sh

COPY ./backend/requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./shared/ /app/shared/
COPY ./backend /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
