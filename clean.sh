#!/bin/sh

docker stop reread-db > /dev/null 2>&1 && docker rm reread-db > /dev/null 2>&1
docker stop reread-mongo > /dev/null 2>&1 && docker rm reread-mongo > /dev/null 2>&1
docker stop reread-web > /dev/null 2>&1 && docker rm reread-web > /dev/null 2>&1
docker stop reread-daemon > /dev/null 2>&1 && docker rm reread-daemon > /dev/null 2>&1
