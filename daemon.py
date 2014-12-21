import os
import django
import threading

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storycafe.settings.production")
django.setup()

from reader.documents import *
from mongoengine import signals


def post_save_notify(sender, document, created):
    print((str(document) + " has been successfully " + ("created" if created else "saved") + ".").encode("utf-8"))

signals.post_save.connect(post_save_notify)


class UpdateSources(threading.Thread):
    def run(self):
        while True:
            for source in Source.objects:
                source.update_articles()


class UpdateReadingLists(threading.Thread):
    def run(self):
        while True:
            for reader in Reader.objects:
                reader.extend_reading_list()

if __name__ == "__main__":
    try:
        HackerNewsSource.objects.get(alias="hackernews")
    except HackerNewsSource.DoesNotExist:
        HackerNewsSource(alias="hackernews", title="Hacker News").save()

    update_sources = UpdateSources()
    update_sources.run()

    update_reading_lists = UpdateReadingLists()
    update_reading_lists.run()
    while True:
        if not update_sources.is_alive():
            update_sources = UpdateSources()
            update_sources.run()
        if not update_reading_lists.is_alive():
            update_reading_lists = UpdateReadingLists()
            update_reading_lists.run()
