from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from reader.documents import *
import datetime
import json
import urllib

@login_required
def subscribe(request, source_id):
    reader = Reader.reader_for(request.user)
    source = Source.objects.get(id=source_id)
    reader.subscribe(source)
    return HttpResponse(json.dumps({"status": "ok"}),
                        content_type="application/json")


@login_required
def unsubscribe(request, source_id):
    reader = Reader.reader_for(request.user)
    source = Source.objects.get(id=source_id)
    reader.unsubscribe(source)
    return HttpResponse(json.dumps({"status": "ok"}),
                        content_type="application/json")
