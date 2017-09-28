#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from df_user import views
urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^register_yz/$',views.register_yz),
    url(r'^register_handler/$',views.register_handler),
    url(r'^login_handler/$',views.login_handler),
    url(r'^info/$',views.info),
    url(r'^center/(\d+)/$',views.center),
    url(r'^pay/(\d+)/(\d+)/$',views.pay),
    url(r'^address/$',views.adress),
    url(r'^orm/$',views.orm),
]
