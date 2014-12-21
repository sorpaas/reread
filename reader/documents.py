from mongoengine import *
import datetime
import urllib
import simplejson as json
import urllib.request as request
from time import mktime
from django.contrib.auth.models import User
from reader.learn import predict_articles


class Source(Document):
    title = StringField(required=True)
    alias = StringField(required=True, unique=True)
    description = StringField()

    def __str__(self):
        return self.title

    def update_articles(self):
        pass

    meta = {'allow_inheritance': True}


class Reader(Document):
    user_id = IntField(required=True, unique=True)
    brain = BinaryField()
    subscriptions = ListField(ReferenceField(Source,
                                             reverse_delete_rule=NULLIFY))
    preferred_article_view = StringField(choices=('frame', 'article'),
                                         default='frame')
    reading_list = ListField(DictField())

    def subscribe(self, source):
        self.update(add_to_set__subscriptions=[source])

    def unsubscribe(self, source):
        self.update(pull_all__subscriptions=[source])

    def is_subscribed(self, source):
        return source in self.subscriptions

    def extend_reading_list(self):
        if len(self.reading_list) > 10:
            return

        if len(ReadRecord.objects(reader=self)) == 0:
            self.update(add_to_set__reading_list=[{"score": 0, "article_id": x.id} for x in Article.objects[:5]])
            return

        predicted = predict_articles(self, Article.objects.filter(
            source__in=self.subscriptions,
            id__nin=[x.article.id for x in ReadRecord.objects(reader=self)] + [x['article_id'] for x in self.reading_list]))
        self.update(add_to_set__reading_list=[{"score": x[1], "article_id": x[0].id} for x in predicted])

    @staticmethod
    def reader_for(user):
        try:
            return Reader.objects.get(user_id=user.id)
        except Reader.DoesNotExist:
            reader = Reader(user_id=user.id)
            reader.save()
            try:
                hackernews = Source.objects.get(alias="hackernews")
            except Source.DoesNotExist:
                hackernews = HackerNewsSource(alias="hackernews", title="Hacker News")
                hackernews.save()
            reader.subscribe(hackernews)
            reader.extend_reading_list()
            return reader


class Article(Document):
    title = StringField(required=True)
    content_text = StringField(required=True)
    content_html = StringField(required=True)
    url = StringField(required=True, unique=True)
    date_published = DateTimeField(required=True,
                                   default=datetime.datetime.now)
    is_framing_allowed = BooleanField(default=True, required=True)
    source = ReferenceField(Source, required=True, reverse_delete_rule=CASCADE)

    meta = {'allow_inheritance': True}

    def update_content_by_url(self):
        from boilerpipe.extract import Extractor
        extractor = Extractor(extractor='ArticleExtractor', url=self.url)
        self.content_html = extractor.getHTML()
        self.content_text = extractor.getText()

    def check_framing_allowed(self):
        from django.conf import settings
        request = urllib.request.Request(self.url)
        request.add_header("Referer", settings.BASE_URL)
        try:
            opener = urllib.request.urlopen(request)
        except Exception:
            self.is_framing_allowed = False
            return
        framing_allowed = not ('x-frame-options' in opener.headers)
        self.is_framing_allowed = framing_allowed

    def __str__(self):
        return (self.title + " [" + self.url + "]")

    @staticmethod
    def get_or_new(**kwargs):
        try:
            return Article.objects.get(**kwargs), False
        except Article.DoesNotExist:
            return Article(**kwargs), True

# Additional Documents for Reader


class ReadRecord(Document):
    reader = ReferenceField(Reader, required=True, unique_with="article")
    article = ReferenceField(Article, required=True, unique_with="reader")
    date_read = ListField(DateTimeField(default=datetime.datetime.now))
    is_liked = BooleanField(default=False, required=True)
    is_learned = BooleanField(default=False, required=True)

# Additional Documents for Articles


class HackerNewsArticle(Article):
    hackernews_id = StringField(required=True)
    hackernews_type = StringField(required=True)
    hackernews_score = IntField(required=True)
    hackernews_submitter = StringField(required=True)

    @staticmethod
    def get_or_new(**kwargs):
        try:
            return HackerNewsArticle.objects.get(**kwargs), False
        except HackerNewsArticle.DoesNotExist:
            return HackerNewsArticle(**kwargs), True

# Additional Documents for Source


class HackerNewsSource(Source):
    def fetch_top_story_ids(self):
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        try:
            story_ids_raw = request.urlopen(top_stories_url)
            return json.loads(story_ids_raw.readlines()[0])
        except Exception:
            return []

    def fetch_story(self, story_id):
        story_url = "https://hacker-news.firebaseio.com/v0/item/{}.json".format(story_id)
        try:
            story_raw = request.urlopen(story_url)
            s = json.loads(story_raw.readlines()[0])
            return s if s['title'] and s['url'] and s['time'] and s['id'] and s['score'] and s['by'] and s['type'] else None
        except Exception:
            return None

    def update_articles(self):
        for story_id in self.fetch_top_story_ids():
            story = self.fetch_story(story_id)
            if not story:
                continue

            article, newed = HackerNewsArticle.get_or_new(url=story['url'])
            article.title = story['title']
            article.date_published = datetime.datetime.fromtimestamp(story['time'])
            article.source = self
            article.hackernews_id = str(story['id'])
            article.hackernews_score = story['score']
            article.hackernews_submitter = story['by']
            article.hackernews_type = story['type']

            try:
                article.update_content_by_url()
            except Exception:
                continue

            article.check_framing_allowed()
            article.save()


class RSSSource(Source):
    url = StringField(required=True)
    categories = ListField(StringField())

    def update_articles(self):
        import feedparser
        try:
            rss = feedparser.parse(self.url)
        except Exception:
            return

        self.title = rss.feed.title

        if hasattr(rss.feed, 'description'):
            self.description = rss.feed.description

        self.save()

        for entry in rss.entries:
            article, newed = Article.get_or_new(url=entry.link)
            article.title = entry.title
            if hasattr(entry, 'published_parsed'):
                article.date_published = datetime.datetime.fromtimestamp(mktime(entry.published_parsed))
            article.source = self

            try:
                article.update_content_by_url()
            except Exception:
                continue

            article.check_framing_allowed()
            article.save()
