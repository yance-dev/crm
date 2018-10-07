#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import OrderedDict
from django.shortcuts import render, HttpResponse, redirect
from django.forms import formset_factory
from django.urls import reverse

from rbac import models
from rbac.service.routes import get_all_url_dict
from rbac.forms.permission import MultiPermissionForm, RoleModelForm, MenuModelForm, PermissionModelForm


def menu_list(request):
    """
    权限管理和分配
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()

    mid = request.GET.get('mid')
    root_permission_list = []
    if mid:
        # 找到可以成为菜单的权限 + 某个菜单下的
        permissions = models.Permission.objects.filter(menu_id=mid).order_by('-id')
    else:
        # 找到可以成为菜单的权限
        permissions = models.Permission.objects.filter(menu__isnull=False).order_by('-id')

    root_permission_queryset = permissions.values('id', 'title', 'url', 'name', 'menu__title')
    root_permission_dict = {}
    for item in root_permission_queryset:
        item['children'] = []
        root_permission_list.append(item)
        root_permission_dict[item['id']] = item

    # 找到可以成为菜单的权限的所有子权限
    node_permission_list = models.Permission.objects.filter(pid__in=permissions).order_by('-id').values('id',
                                                                                                        'title',
                                                                                                        'url',
                                                                                                        'name',
                                                                                                        'pid')
    for node in node_permission_list:
        pid = node['pid']
        root_permission_dict[pid]['children'].append(node)

    return render(
        request,
        'rbac/menu_list.html',
        {
            'menu_list': menus,
            'root_permission_list': root_permission_list,
            'mid': mid
        }
    )


def menu_add(request):
    """
    添加菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
    else:
        form = MenuModelForm(request.POST)
        if form.is_valid():
            print(form.data)
            form.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/menu_change.html', {'form': form})


def menu_edit(request, pk):
    """
    编辑菜单
    :param request:
    :return:
    """
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/menu_change.html', {'form': form})

    form = MenuModelForm(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:menu_list'))


def menu_del(request, pk):
    """
    删除菜单
    :param request:
    :param pk:
    :return:
    """
    models.Menu.objects.filter(id=pk).delete()
    return redirect(reverse('rbac:menu_list'))


def permission_add(request):
    """
    添加权限
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
    else:
        form = PermissionModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/permission_change.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :return:
    """
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('权限不存在')

    if request.method == 'GET':
        form = PermissionModelForm(instance=obj)
    else:
        form = PermissionModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/permission_change.html', {'form': form})


def permission_del(request, pk):
    """
    删除权限
    :param request:
    :return:
    """
    models.Permission.objects.filter(id=pk).delete()
    return redirect(request.META['HTTP_REFERER'])


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')

    MultiPermissionFormSet = formset_factory(MultiPermissionForm, extra=0)
    generate_formset = None
    update_formset = None

    if request.method == 'POST' and post_type == 'generate':
        formset = MultiPermissionFormSet(request.POST)
        if not formset.is_valid():
            generate_formset = formset
        else:
            for row_dict in formset.cleaned_data:
                row_dict.pop('id')
                models.Permission.objects.create(**row_dict)

    if request.method == 'POST' and post_type == 'update':
        formset = MultiPermissionFormSet(request.POST)
        if formset.is_valid():
            for row_dict in formset.cleaned_data:
                permission_id = row_dict.pop('id')
                models.Permission.objects.filter(id=permission_id).update(**row_dict)
        else:
            update_formset = formset

    # 1.1 去数据库中获取所有权限
    # [{},{}]
    permissions = models.Permission.objects.all().values('id', 'title', 'url', 'name', 'menu_id', 'pid_id')
    # {'rbac:menu_list':{},'rbac:menu_add':{..}}
    permisssion_dict = OrderedDict()
    for per in permissions:
        permisssion_dict[per['name']] = per

    # 1.2 数据库中有的所有权限name的集合
    permission_name_set = set(permisssion_dict.keys())


    # 2.1 获取路由系统中所有的URL
    # {'rbac:menu_list':{'url':.... },,,}
    router_dict = get_all_url_dict(ignore_namespace_list=['admin'])

    for row in permissions:
        name = row['name']
        if name in router_dict:
            router_dict[name].update(row)

    # 2.2 路由系统中的所有权限name的集合
    router_name_set = set(router_dict.keys())

    # 需要新建：数据库无、路由有
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = MultiPermissionFormSet(
            initial=[row for name, row in router_dict.items() if name in generate_name_list])

    # 需要删除：数据库有、路由无
    destroy_name_list = permission_name_set - router_name_set
    destroy_formset = MultiPermissionFormSet(
        initial=[row for name, row in permisssion_dict.items() if name in destroy_name_list])

    # 需要更新：数据库有、路由有
    if not update_formset:
        update_name_list = permission_name_set.intersection(router_name_set)
        update_formset = MultiPermissionFormSet(
            initial=[row for name, row in router_dict.items() if name in update_name_list])

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'destroy_formset': destroy_formset,
            'update_formset': update_formset,
            'generate_formset': generate_formset,
        }
    )


def distribute_permissions(request):
    """
    分配权限
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    from django.utils.module_loading import import_string
    from django.conf import settings
    user_class = import_string(settings.USER_MODEL_PATH)

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        # 更新选择用户所拥有的角色
        user = user_class.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    user_list = user_class.objects.all()
    # ############################## 角色信息 ##########################
    # 当前用户拥有的角色
    user_has_roles = user_class.objects.filter(id=uid).values('id', 'roles')
    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    # 所有的角色
    role_list = models.Role.objects.all()

    # ############################## 权限信息 ##########################
    all_menu_list = []

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid, permissions__id__isnull=False).values('id',
                                                                                                        'permissions')
    elif uid and not rid:
        user = user_class.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.filter(permissions__id__isnull=False).values('id', 'permissions')
    else:
        role_has_permissions = []

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    # 菜单
    queryset = models.Menu.objects.values('id', 'title')
    menu_dict = {}
    for item in queryset:
        item['children'] = []
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    # 根权限
    root_permission = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    root_permission_dict = {}
    for per in root_permission:
        per['children'] = []
        nid = per['id']
        menu_id = per['menu_id']
        # print(nid, menu_id)
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    # 子权限
    node_permission = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    for per in node_permission:
        pid = per['pid_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': user_list,
            'role_list': role_list,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'all_menu_list': all_menu_list,
            'uid': uid,
            'rid': rid
        }
    )


def role_list(request):
    """
    角色管理
    :param request:
    :return:
    """
    form = RoleModelForm()
    if request.method == 'POST':
        form = RoleModelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('rbac:role_list'))
    roles = models.Role.objects.all().order_by('-id')
    return render(request, 'rbac/role_list.html', {'roles': roles, 'form': form})


def role_edit(request, pk):
    """
    编辑角色
    :param request:
    :param pk:
    :return:
    """
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
    else:
        form = RoleModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/role_change.html', {'form': form})


def role_del(request, pk):
    """
    删除角色
    :param request:
    :param pk:
    :return:
    """
    models.Role.objects.filter(id=pk).delete()
    return redirect(reverse('rbac:role_list'))
