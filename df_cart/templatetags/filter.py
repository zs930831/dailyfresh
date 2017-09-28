#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django import template

#文件夹的名字templatetags不能改，写在app下，register也不能变
register = template.Library()

#simple_tag可以有多个参数，不可以放在if后面
# @register.simple_tag
# def jf(a1,a2):
#     return a1 + a2

#filter只能有2个参数，可以放在if后面
@register.filter
def lenCart(a1,a2):
    return(len(a1))


