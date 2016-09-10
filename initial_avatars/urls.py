# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from .views import avatar

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', avatar, name='avatar'),
    url(r'^(?P<id>[0-9]+)/(?P<size>[0-9]{2,3})/$', avatar, name='avatar'),
]
