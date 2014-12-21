from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from reader.documents import *
import datetime
import json
import urllib

@login_required
def like_article(request, record_id):
    record = ReadRecord.objects.get(id=record_id)
    record.is_liked = True
    record.save()
    return HttpResponse(json.dumps({"status": "ok"}),
                        content_type="application/json")

@login_required
def unlike_article(request, record_id):
    record = ReadRecord.objects.get(id=record_id)
    record.is_liked = False
    record.save()
    return HttpResponse(json.dumps({"status": "ok"}),
                        content_type="application/json")

@login_required
def create(request, article_id):
    reader = Reader.reader_for(request.user)
    article = Article.objects.get(id=article_id)
    reader.reading_list = [x for x in reader.reading_list if str(x['article_id']) != str(article_id)]
    reader.save()
    try:
        record = ReadRecord.objects.get(reader=reader, article=article)
    except ReadRecord.DoesNotExist:
        record = ReadRecord(reader=reader, article=article)
        record.save()
    return HttpResponse(json.dumps({"status": "ok",
                                    "record_id": str(record.id),
                                    "is_liked": record.is_liked}),
                        content_type="application/json")
