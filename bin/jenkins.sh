#!/bin/bash
set -e

# Wait for postgres to come up
sleep 5s;

# Run the tests
./manage.py test

if [ ! "$DOTCI_BRANCH" == "dotci2" ];
then
    echo "Not on master branch, not pushing to docker hub.";
    exit 0;
fi
if [ -z "$DOCKER_USERNAME" ];
then
    echo "Docker username is unset, not pushing to docker hub.";
    exit 0;
fi
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD -e $DOCKER_EMAIL
docker tag -f dockerfile giorgos/masterfirefoxos:$DOTCI_SHA
docker push giorgos/masterfirefoxos:$DOTCI_SHA
