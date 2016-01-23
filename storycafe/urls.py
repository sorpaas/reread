from django.conf.urls import include, url
from django.contrib import admin, auth
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/reader/')),
    url(r'^accounts/$', RedirectView.as_view(url='/reader/')),
    url(r'^reader/', include('reader.urls')),
    url(r'^', include('home.urls')),
]
