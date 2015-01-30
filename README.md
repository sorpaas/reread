Reread: Yet Another Hacker News Reader
======
Reread is my personal Hacker News Reader. It is hackable and easy to deploy. A
hosted version of Reread can be found at [reread.io](http://reread.io).

![Reread Screenshot](https://github.com/sorpaas/reread/raw/master/screenshot.png)

## Features

* **Read Hacker News**
* Read RSS Feed
* Hackable
* A Little Bit Machine Learning
* Subscriptions

## Why Another News Reader?

Because privacy and control of data becomes even more important when we want to
add a little Machine Learning in the tools we use. And hackable and fun things
are always better than anything else.

## Install

Reread can be built with [Docker](http://docker.io). Once you have docker
installed, simply run:

    ./build.sh

And a running instance will be accessable at http://localhost:8000

## Configuration

There are several variables in `./build.sh` that you need to configure if you want to deploy
Reread into a production environment.

* **DB_DIR**: The Postgresql DB files directory.
* **MONGO_DIR**: The Mongo DB files directory.
* **SECRET_KEY**: A secret key that needs keeping secretly. It can be generated
  easily with things like [this](https://gist.github.com/ndarville/3452907).
* **REREAD_ENV**: Change this to `storycafe.settings.production` for production
environment.
* **REREAD_PORT**: The port that will be publicly served. Default to 8000.
* **REREAD_HOST**: The domain name that you want to host for production environment.

## Hacking the Learning Model

Currently the predict function in `reader/learn.py` is really naive, but I
found it already enough for personal use. If you want ot hack it, simply modify
the `predict_articles` function in `reader/learn.py`.
