Reread: Yet Another Hacker News Reader
======
Reread is my personal Hacker News Reader. It is hackable and easy to deploy. A
hosted version of Reread can be found at [reread.id.hn](http://reread.id.hn/).

![Reread Screenshot](https://cdn.source.id.hn/file/data/xpbmrg3mussgttifodwq/PHID-FILE-vqcl2nmdqqos2fsiz4aj/5y7wi6pjaw7terfu/Reread_Screenshot)

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

Reread can be built with [Docker](http://docker.io) with Docker Compose. Once
you have them installed, simply run:

    docker-compose up

And a running instance will be accessable at http://localhost:3020

## Configuration

There are several variables in `./docker-compose.yml` that you need to configure
if you want to deploy Reread into a production environment.

* **SECRET_KEY**: A secret key that needs keeping secretly. It can be generated
  easily with things like [this](https://gist.github.com/ndarville/3452907).
* **DJANGO_SETTINGS_MODULE**: Change this to `storycafe.settings.production` for
production environment.

## Hacking the Learning Model

Currently the predict function in `reader/learn.py` is really naive, but I
found it already enough for personal use. If you want ot hack it, simply modify
the `predict_articles` function in `reader/learn.py`.

## Issues and Contribution

The project is managed at a [Phabricator instance](https://source.id.hn/).
[Create a new issue](https://source.id.hn/maniphest/task/edit/form/default/?projects=reread).
