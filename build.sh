#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DB_DIR="$DIR/.db"
MONGO_DIR="$DIR/.mongo"
SECRET_KEY="yourawesomesecretkey"
REREAD_ENV="storycafe.settings.development"
REREAD_PORT="8000"
REREAD_HOST="reread.io"

docker start reread-db > /dev/null 2>&1

if [ $? -ne 0 ]
then
    echo "Reread DB does not exist, creating one ..."
    docker run -v $DB_DIR:/var/lib/postgresql/data --name reread-db -d postgres
    sleep 2
    docker exec -i -t reread-db createdb -h localhost -U postgres storycafe
fi
sleep 10

docker start reread-mongo > /dev/null 2>&1
if [ $? -ne 0 ]
then
    echo "Reread Mongo does not exist, creating one ..."
    docker run -v $MONGO_DIR:/data/db --name reread-mongo -d mongo
fi
sleep 10

if [ ! -f $DIR/.docker-built ]
then
    echo "Building Reread Web Application ..."
    docker build --tag=sorpaas/reread $DIR
    touch $DIR/.docker-built
fi

docker start reread-web > /dev/null 2>&1
if [ $? -ne 0 ]
then
    echo "Reread Web does not exist, creating one ..."
    docker run -e DJANGO_SETTINGS_MODULE=$REREAD_ENV -e SECRET_KEY=$SECRET_KEY -e REREAD_HOST=$REREAD_HOST -v $DIR:/app --publish=127.0.0.1:8000:$REREAD_PORT -d --link=reread-db:db --link=reread-mongo:mongo --name=reread-web sorpaas/reread
fi

docker start reread-daemon > /dev/null 2>&1
if [ $? -ne 0 ]
then
    echo "Reread Daemon does not exist, creating one ..."
    docker run -e DJANGO_SETTINGS_MODULE=$REREAD_ENV -e SECRET_KEY=$SECRET_KEY -e REREAD_HOST=$REREAD_HOST -v $DIR:/app -d --link=reread-db:db --link=reread-mongo:mongo --name=reread-daemon sorpaas/reread python daemon.py
fi

echo
echo "Reread started successfully. Now you can go to http://localhost:8000 and start reading."
