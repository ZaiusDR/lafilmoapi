#!/bin/bash

set -ue

source .env

heroku local:run python manage.py runserver
