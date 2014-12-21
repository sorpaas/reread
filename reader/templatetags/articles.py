from django import template
from reader.documents import *

register = template.Library()

@register.filter(name='is_hacker_news_article')
def is_hacker_news_article(article):
    return isinstance(article, HackerNewsArticle)
