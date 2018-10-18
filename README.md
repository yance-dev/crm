# [django——CRM项目](https://www.cnblogs.com/huang-yc/p/9697938.html)



## 1.引言

CRM，客户关系管理系统（Customer Relationship Management）。企业用CRM技术来管理与客户之间的关系，以求提升企业成功的管理方式，其目的是协助企业管理销售循环：新客户的招徕、保留旧客户、提供客户服务及进一步提升企业和客户的关系，并运用市场营销工具，提供创新式的个人化的客户商谈和服务，辅以相应的信息系统或信息技术如数据挖掘和数据库营销来协调所有公司与顾客间在销售、营销以及服务上的交互。

此系统主要是以教育行业为背景，为公司开发的一套客户关系管理系统。为了扩大的系统使用范围，特此将该项目开发改为组件化开发，让同学们可以日后在自己公司快速搭建类似系统及新功能扩展。

- 权限系统，一个独立的rbac组件。
- stark组件，一个独立的curd组件。
- crm业务，以教育行业为背景并整合以上两个组件开发一套系统。

![img](https://img2018.cnblogs.com/blog/1356841/201809/1356841-20180925092527204-1527825277.png)

## 基于组件的软件工程：

 基于组件的软件工程（*Component-based software engineering*，简称*CBSE*）或基于组件的开发（*Component-Based Development*，简称CBD）是一种软件开发范型。它是现今[软件复用](https://baike.baidu.com/item/%E8%BD%AF%E4%BB%B6%E5%A4%8D%E7%94%A8)理论实用化的研究热点，在[组件对象模型](https://baike.baidu.com/item/%E7%BB%84%E4%BB%B6%E5%AF%B9%E8%B1%A1%E6%A8%A1%E5%9E%8B)的支持下，通过复用已有的[构件](https://baike.baidu.com/item/%E6%9E%84%E4%BB%B6)，软件开发者可以“[即插即用](https://baike.baidu.com/item/%E5%8D%B3%E6%8F%92%E5%8D%B3%E7%94%A8)”地快速构造[应用软件](https://baike.baidu.com/item/%E5%BA%94%E7%94%A8%E8%BD%AF%E4%BB%B6)。

**优势：**

这样不仅可以节省时间和经费，提高工作效率，而且可以产生更加规范、更加可靠的[应用软件](https://baike.baidu.com/item/%E5%BA%94%E7%94%A8%E8%BD%AF%E4%BB%B6)。

**模型：**

![img](https://img2018.cnblogs.com/blog/1356841/201810/1356841-20181006161607713-193330368.png)

 

## 2.项目表设计：

![img](https://img2018.cnblogs.com/blog/1356841/201810/1356841-20181018205058883-1659294088.png)

 *ps:右键，新窗口打开查看大图*

## 3.stark组件使用说明：

```
 1 使用stark组件需要完成一下几个步骤：
 2 1. 拷贝stark app到任何系统。
 3 2. 在目标project中注册stark app，如：
 4     INSTALLED_APPS = [
 5         ...
 6         'stark.apps.StarkConfig',
 7     ]
 8 3. 如果想要使用stark组件，则需要在目标app的根目录中创建 stark.py
 9 4. 配置路由信息
10     from stark.service.stark import site
11     urlpatterns = [
12         ...
13         url(r'^stark/', site.urls),
14     ]
15 
16 5. 接下来就可以使用stark组件进行快速增删改查,示例：
17     from crm import models
18     from stark.service.stark import site, StarkConfig
19     from django.utils.safestring import mark_safe
20     from django.conf.urls import url
21     from django.shortcuts import HttpResponse
22     from django.urls import reverse
23     from crm.config.class_list import ClassListConfig
24 
25     class DepartmentConfig(StarkConfig):
26         list_display = ['id', 'title', StarkConfig.display_edit, StarkConfig.display_del]
27 
28 
29     site.register(models.Department, DepartmentConfig)
30 
31 
32     class UserInfoConfig(StarkConfig):
33 
34         def display_gender(self, row=None, header=False):
35             if header:
36                 return '性别'
37             return row.get_gender_display()
38 
39         def display_detail(self,row=None, header=False):
40             if header:
41                 return '查看详细'
42             return mark_safe('<a href="%s">%s</a>' %(reverse('stark:crm_userinfo_detail',kwargs={'pk':row.id}),row.name,))
43 
44         list_display = [
45             display_detail,
46             display_gender,
47             'phone',
48             'email',
49             'depart',
50             StarkConfig.display_edit,
51             StarkConfig.display_del
52         ]
53 
54         def extra_url(self):
55             info = self.model_class._meta.app_label, self.model_class._meta.model_name
56 
57             urlpatterns = [
58                 url(r'^(?P<pk>\d+)/detail/$', self.wrapper(self.detail_view), name='%s_%s_detail' % info),
59             ]
60             return urlpatterns
61 
62         def detail_view(self,request,pk):
63             """
64             查看详细页面
65             :param request:
66             :param pk:
67             :return:
68             """
69             return HttpResponse('详细页面...')
70 
71         search_list = ['name','depart__title']
72 
73 
74     site.register(models.UserInfo, UserInfoConfig)
```

## 4.rbac权限组件使用说明：

```
 1 使用rbac组件时，应用遵循以下规则：
 2 
 3 1. 清除rbac/migrations目录下所有数据库迁移记录（保留__init__.py）
 4 
 5 2. 在项目路由系统中注册rabc相关的路由信息，如：
 6     urlpatterns = [
 7         ...
 8         url(r'^rbac/', include('rbac.urls',namespace='rbac')),
 9     ]
10 
11 3. 注册app
12 
13 4. 让业务的用户表继承权限的UserInfo表
14     如：
15         rbac:
16             class UserInfo(models.Model):
17                 """
18                 用户表
19                 """
20                 username = models.CharField(verbose_name='用户名', max_length=32)
21                 password = models.CharField(verbose_name='密码', max_length=64)
22                 email = models.CharField(verbose_name='邮箱', max_length=32)
23                 roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)
24 
25                 class Meta:
26                     abstract = True
27         crm:
28             from rbac.models import UserInfo as RbacUserInfo
29             class UserInfo(RbacUserInfo):
30                 """
31                 员工表
32                 """
33                 name = models.CharField(verbose_name='真实姓名', max_length=16)
34                 phone = models.CharField(verbose_name='手机号', max_length=32)
35 
36                 gender_choices = (
37                     (1,'男'),
38                     (2,'女'),
39                 )
40                 gender = models.IntegerField(verbose_name='性别',choices=gender_choices,default=1)
41 
42                 depart = models.ForeignKey(verbose_name='部门', to="Department")
43 
44                 def __str__(self):
45                     return self.name
46 
47 5. 数据库迁移
48 
49 6. rbac提供URL
50     urlpatterns = [
51         url(r'^menu/list/$', permission.menu_list, name='menu_list'), # rbac:menu_list
52         url(r'^menu/add/$', permission.menu_add, name='menu_add'),
53         url(r'^menu/edit/(?P<pk>\d+)/$', permission.menu_edit, name='menu_edit'),
54         url(r'^menu/del/(?P<pk>\d+)/$', permission.menu_del, name='menu_del'),
55         url(r'^permission/add/$', permission.permission_add, name='permission_add'),
56         url(r'^permission/edit/(?P<pk>\d+)/$', permission.permission_edit, name='permission_edit'),
57         url(r'^permission/del/(?P<pk>\d+)/$', permission.permission_del, name='permission_del'),
58 
59         url(r'^multi/permissions/$', permission.multi_permissions, name='multi_permissions'),
60 
61         url(r'^distribute/permissions/$', permission.distribute_permissions, name='distribute_permissions'),
62         url(r'^role/list/$', permission.role_list, name='role_list'),
63         url(r'^role/edit/(?P<pk>\d+)/$', permission.role_edit, name='role_edit'),
64         url(r'^role/del/(?P<pk>\d+)/$', permission.role_del, name='role_del'),
65     ]
```
