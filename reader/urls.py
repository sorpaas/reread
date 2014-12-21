from django.conf.urls import patterns, url
from reader.views import articles, subscriptions
import reader.views.queries.read_records as queries_read_records
import reader.views.queries.subscriptions as queries_subscriptions

urlpatterns = patterns('',
                       url(r'^article/(?P<article_id>[a-z0-9]+)$',
                           articles.show, name='show'),
                       url(r'^$',
                           articles.select, name='select'),
                       url(r'^subscriptions/$',
                           subscriptions.index),

                       url(r'^query/read_records/like/(?P<record_id>[0-9a-z]+)$', queries_read_records.like_article),
                       url(r'^query/read_records/unlike/(?P<record_id>[0-9a-z]+)$', queries_read_records.unlike_article),
                       url(r'^query/read_records/create/(?P<article_id>[0-9a-z]+)$', queries_read_records.create),
                       url(r'^query/subscriptions/subscribe/(?P<source_id>[0-9a-z]+)$', queries_subscriptions.subscribe),
                       url(r'^query/subscriptions/unsubscribe/(?P<source_id>[0-9a-z]+)$', queries_subscriptions.unsubscribe),
)
