#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.template import Library
from django.conf import settings
from collections import OrderedDict
from django.urls import reverse
from urllib.parse import urlencode

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """生成菜单"""

    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    key_list = sorted(menu_dict)

    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            if per['id'] == request.current_permission_pid:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val
    return {
        'menu_dict': ordered_dict
    }


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """生成路径导航"""
    return {
        'breadcrumb_list': request.current_breadcrumb_list
    }


@register.filter
def has_permission(request, name):
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
    if name in permission_dict:
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()
