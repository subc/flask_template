#!/bin/sh

GUNICORN=$HOME/.virtualenvs/matome/bin/gunicorn
PROJECT_ROOT=/var/flask/matome/matome

APP=wsgi:app

cd $PROJECT_ROOT
exec $GUNICORN -c $PROJECT_ROOT/config/gunicorn/gunicorn.conf.py $APP
