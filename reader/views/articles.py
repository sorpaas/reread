from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from reader.documents import *
import datetime
from reader.helpers import build_url, redirect_link_with_params


@login_required
def select(request):
    reader = Reader.reader_for(request.user)
    if len(reader.reading_list) == 0:
        reader.extend_reading_list()
        reader = Reader.reader_for(request.user)
        if len(reader.reading_list) == 0:
            return HttpResponseRedirect('/reader/subscriptions')

    article = Article.objects.get(id=reader.reading_list[0]['article_id'])

    param_view = request.GET.get('type')
    param_next = request.path

    return show(request, str(article.id),
                view=param_view,
                next=param_next,
                history_link=redirect_link_with_params(
                    'show', article.id,
                    view=param_view,
                    next=param_next))


def show(request, article_id, **kwargs):
    VIEW_TEMPLATES = {
        'frame': 'reader/frame.html',
        'article': 'reader/article.html',
    }
    DEFAULT_VIEW = 'article'
    DEFAULT_NEXT_LINK = '/reader'

    article = Article.objects.get(id=article_id)
    next_link = kwargs.get('next') or request.GET.get('next') or DEFAULT_NEXT_LINK
    history_link = kwargs.get('history_link')
    view = kwargs.get('view') or request.GET.get('view') or DEFAULT_VIEW

    def article_view_link():
        return build_url('/reader/article/' + article_id, view='article',
                         next=next_link)

    def frame_view_link():
        return build_url('/reader/article/' + article_id, view='frame',
                         next=next_link)

    if request.user.is_authenticated():
        reader = Reader.reader_for(request.user)
        reader.preferred_article_view = kwargs.get('view') or request.GET.get('view') or reader.preferred_article_view
        reader.save()
        view = reader.preferred_article_view
        predicted_articles = [(Article.objects.get(id=x['article_id']), x['score']) for x in reader.reading_list]

    if not article.is_framing_allowed:
        view = 'article'

    return render(request, VIEW_TEMPLATES[view], {
        'article': article,
        'next_link': next_link,
        'article_view_link': article_view_link(),
        'frame_view_link': frame_view_link(),
        'predicted_articles': predicted_articles,
        'history_link': history_link})
