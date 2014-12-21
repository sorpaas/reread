Reread: Yet Another Hacker News Reader
======
Reread is a hackable Hacker News / RSS Reader. It is easy to deploy and built
upon Docker. A hosted version of Reread can be found at
[reread.io](http://reread.io).

## Features

* Simple.
* Hackable
* Read while learning your preference (a.k.a Machine Learning).
* Subscriptions.

## Install

Reread is built upon Docker. Please make sure you have
[Docker](http://docker.io) installed before installing Reread.

Install Reread is easy, simply run:

    ./build.sh

And a running instance will be accessable at http://localhost:8000

## Configuration

There are several variables that you need to configure if you want to deploy
Reread into a production environment in `./build.sh`

* **DB_DIR**: The Postgresql DB files directory.
* **MONGO_DIR**: The Mongo DB files directory.
* **SECRET_KEY**: A secret key that needs keeping secretly.
* **REREAD_ENV**: Change this to `storycafe.settings.production` for production
environment.
* **REREAD_PORT**: The port that will be publicly served. Default to 8000.
* **REREAD_HOST**: The domain name that you want to host.

## Building the Machine Learning Model

The default Machine Learning Model is simple and only take advantages of the
content texts. I found it already enough to filter interesting news from boring
ones. However, there are many other features that may be of use.

In order to hack the model, simply modify the `predict_articles` in
`reader/learn.py`.
