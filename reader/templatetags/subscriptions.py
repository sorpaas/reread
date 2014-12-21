from django import template
from reader.documents import *

register = template.Library()

@register.filter(name='js_is_subscribed')
def js_is_subscribed(source, reader):
    return "true" if reader.is_subscribed(source) else "false"

@register.filter(name='is_subscribed')
def is_subscribed(source, reader):
    return reader.is_subscribed(source)
