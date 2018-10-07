from crm import models
from stark.service.stark import site, StarkConfig,get_choice_text
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.conf import settings
from crm.config.class_list import ClassListConfig
from crm.config.customer import CustomerConfig,PublicCustomerConfig,PrivateCustomerConfig
from crm.config.consult_record import ConsultRecordConfig,PriConsultRecordConfig
from crm.config.student import StudentConfig
from crm.config.course_record import CourseRecordConfig
from crm.config.study_record import StudyRecordConfig

from crm.permission.base import RbacPermission

class DepartmentConfig(StarkConfig):
    list_display = ['id', 'title', StarkConfig.display_edit, StarkConfig.display_del]


site.register(models.Department, DepartmentConfig)




class UserInfoConfig(StarkConfig):

    def display_detail(self,row=None, header=False):
        if header:
            return '查看详细'
        return mark_safe('<a href="%s">%s</a>' %(reverse('stark:crm_userinfo_detail',kwargs={'pk':row.id}),row.name,))

    list_display = [
        display_detail,
        get_choice_text('gender','性别'), # display_gender函数：self, row=None, header=False
        'phone',
        'email',
        'depart',
        StarkConfig.display_edit,
        StarkConfig.display_del
    ]

    def extra_url(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name

        urlpatterns = [
            url(r'^(?P<pk>\d+)/detail/$', self.wrapper(self.detail_view), name='%s_%s_detail' % info),
        ]
        return urlpatterns

    def detail_view(self,request,pk):
        """
        查看详细页面
        :param request:
        :param pk:
        :return:
        """
        return HttpResponse('详细页面...')

    search_list = ['name','depart__title']


site.register(models.UserInfo, UserInfoConfig)


class CourseConfig(RbacPermission,StarkConfig):
    list_display = ['id','name']


site.register(models.Course,CourseConfig)


class SchoolConfig(RbacPermission,StarkConfig):

    list_display = ['id','title']



site.register(models.School,SchoolConfig)
site.register(models.ClassList,ClassListConfig)
site.register(models.Customer,CustomerConfig)
site.register(models.Customer,PublicCustomerConfig,'pub')
site.register(models.Customer,PrivateCustomerConfig,'pri')
site.register(models.ConsultRecord,ConsultRecordConfig)
site.register(models.ConsultRecord,PriConsultRecordConfig,'pri')
site.register(models.Student,StudentConfig)
site.register(models.CourseRecord,CourseRecordConfig)
site.register(models.StudyRecord,StudyRecordConfig)



