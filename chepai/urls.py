"""chepai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'polls.views.login', name='login'),
    url(r'^dologin$', 'polls.views.dologin', name='dologin'),
    url(r'^mainpage$', 'polls.views.mainpage', name='mainpage'),
    url(r'^train$', 'polls.views.train', name='train'),
    url(r'^fight$', 'polls.views.fight', name='fight'),
    url(r'^getTrainPhoto$', 'polls.views.getTrainPhoto', name='getTrainPhoto'),
    url(r'^uploadPic$', 'polls.views.uploadPic', name='uploadPic'),
    url(r'^getCodeImg$', 'polls.views.getCodeImg', name='getCodeImg'),
    url(r'^setCode$', 'polls.views.setCode', name='setCode'),
    url(r'^setTimeStamp$', 'polls.views.setTimeStamp', name='setTimeStamp'),
    url(r'^getTimeStamp$', 'polls.views.getTimeStamp', name='getTimeStamp'),
    url(r'^getCode$', 'polls.views.getCode', name='getCode'),
    url(r'^getVersion$', 'polls.views.getVersion', name='getVersion'),
    url(r'^getVersionContent$', 'polls.views.getVersionContent', name='getVersionContent'),
    url(r'^setVersionContent$', 'polls.views.setVersionContent', name='setVersionContent'),
    url(r'^getOrderInfo$', 'polls.views.getOrderInfo', name='getOrderInfo'),
    url(r'^gettest$', 'polls.views.gettest', name='gettest'),
    url(r'^gettesttime$', 'polls.views.gettesttime', name='gettesttime'),
]

if settings.DEBUG is False:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATIC_ROOT,
                            }),
                            )
