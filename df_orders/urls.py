#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from df_orders import views
urlpatterns = [
    url(r'^$', views.order),
    url(r'^order_handler/', views.order_handler),
]
