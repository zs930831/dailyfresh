#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.shortcuts import redirect
from django.http import  HttpResponseRedirect
def login_dec(func):
    def inner(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            #print("do not jump to %s"%("login"))
            return func(request,*args,**kwargs)
        else:
            #red=redirect('/user/login/')
            red=HttpResponseRedirect('/user/login/')
            #print("jump to %s"%("login"))
            red.set_cookie('url',request.get_full_path())
            return red
    return inner