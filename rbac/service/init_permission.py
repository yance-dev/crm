#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf import settings


def init_permission(user, request):
    """
    用户权限初始化
    :param user: 用户对象
    :param request: 请求相关
    :return:
    """

    # 根据角色获取所有权限
    permission_list = user.roles.filter(permissions__id__isnull=False).values('permissions__id',
                                                                              'permissions__title',
                                                                              'permissions__url',
                                                                              'permissions__name',
                                                                              'permissions__pid_id',
                                                                              'permissions__pid__url',
                                                                              'permissions__pid__name',
                                                                              'permissions__menu_id',
                                                                              'permissions__menu__title',
                                                                              'permissions__menu__icon',
                                                                              ).distinct()

    menu_dict = {}
    permission_dict = {}
    for item in permission_list:
        # 处理权限
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid_id'],
            'pid_url': item['permissions__pid__url'],
            'pid_name': item['permissions__pid__name'],
        }

        # 处理菜单
        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue
        menu_node = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url']
        }
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(menu_node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [
                    menu_node
                ]
            }

    # 将权限信息和菜单信息 放入session
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
