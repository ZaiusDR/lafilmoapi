FROM python:3.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY requirements.txt .

RUN apk update \
    && apk add --update --no-cache --virtual build-deps \
        gcc python3-dev musl-dev \
        libxslt-dev g++ libxslt-dev \
    && apk add postgresql-dev libxslt  \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-deps

COPY . .

RUN python manage.py collectstatic --noinput

RUN adduser -D django
USER django

CMD gunicorn lafilmoapi.wsgi:application --bind 0.0.0.0:$PORT
