from django.conf.urls import patterns, include, url
from polls import views

urlpatterns = patterns('',
    url(r'^dologin$', views.dologin, name='dologin'),
)