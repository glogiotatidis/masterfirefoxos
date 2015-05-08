#!/bin/sh


if [ -e ./.git/HEAD ]
then
    cp ./.git/HEAD /app/masterfirefoxos/base/static/revision.txt
else
    echo $GIT_SHA > /app/masterfirefoxos/base/static/revision.txt
fi

./bin/run-common.sh
./manage.py collectstatic --noinput
gunicorn masterfirefoxos.wsgi:application --preload -b 0.0.0.0:80 -w 2 --log-file -
