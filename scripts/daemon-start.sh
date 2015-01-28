#!/bin/sh

until PGPASSWORD=postgres psql -l -U reread -h db; do
    echo "Postgres not ready, retrying ..."
done

python manage.py migrate

until python daemon.py; do
    echo "Server dies, restarting ..."
    sleep 1
done
