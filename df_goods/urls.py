#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from df_goods import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^(P?<gid>\d+)/$', views.detail),
    url(r'^(\d+)_(\d+)_(\d+)/$', views.list),
]
