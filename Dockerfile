FROM base/archlinux
MAINTAINER Wei Tang <hi@beyond.codes>

RUN pacman -Sy archlinux-keyring --noconfirm
RUN pacman -Syyu --noconfirm
RUN pacman-db-upgrade
RUN pacman -S --noconfirm python-django python-scikit-learn python-beautifulsoup4 python-lxml python-pip jdk8-openjdk gcc ruby postgresql-libs python-psycopg2 make python-nltk
ENV PATH /root/.gem/ruby/2.3.0/bin:$PATH

RUN gem install sass compass
RUN pip install django-guardian boilerpipe-py3 feedparser markdown simplejson django-allauth django_compressor mongoengine blinker

RUN mkdir /app
ADD . /app
WORKDIR /app

EXPOSE 8000
