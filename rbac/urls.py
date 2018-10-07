from django.conf.urls import url
from rbac.views import permission

urlpatterns = [

    url(r'^menu/list/$', permission.menu_list, name='menu_list'), # rbac:menu_list
    url(r'^menu/add/$', permission.menu_add, name='menu_add'),
    url(r'^menu/edit/(?P<pk>\d+)/$', permission.menu_edit, name='menu_edit'),
    url(r'^menu/del/(?P<pk>\d+)/$', permission.menu_del, name='menu_del'),
    url(r'^permission/add/$', permission.permission_add, name='permission_add'),
    url(r'^permission/edit/(?P<pk>\d+)/$', permission.permission_edit, name='permission_edit'),
    url(r'^permission/del/(?P<pk>\d+)/$', permission.permission_del, name='permission_del'),

    url(r'^multi/permissions/$', permission.multi_permissions, name='multi_permissions'),

    url(r'^distribute/permissions/$', permission.distribute_permissions, name='distribute_permissions'),
    url(r'^role/list/$', permission.role_list, name='role_list'),
    url(r'^role/edit/(?P<pk>\d+)/$', permission.role_edit, name='role_edit'),
    url(r'^role/del/(?P<pk>\d+)/$', permission.role_del, name='role_del'),

]
