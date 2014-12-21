from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from reader.documents import *


@login_required
def index(request):
    reader = Reader.reader_for(request.user)
    from django import forms

    class RSSForm(forms.Form):
        title = forms.CharField(label='Title', max_length=100,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Title'}))
        link = forms.CharField(label="Link", max_length=250,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'RSS Url'}))

    if request.method == 'POST':
        form = RSSForm(request.POST)
        if form.is_valid():
            try:
                rss_source = RSSSource.objects.get(url=form.cleaned_data['link'])
            except RSSSource.DoesNotExist:
                rss_source = RSSSource(title=form.cleaned_data['title'],
                                       alias="rss::" + form.cleaned_data['link'],
                                       url=form.cleaned_data['link'])
                rss_source.save()
                reader.subscribe(rss_source)
        return HttpResponseRedirect('/reader/subscriptions')

    rss_form = RSSForm()
    source_list = Source.objects

    return render(request, 'reader/subscriptions.html',
                  {'source_list': source_list,
                   'rss_form': rss_form,
                   'reader': reader})
