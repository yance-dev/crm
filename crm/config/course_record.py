from crm import models
from stark.service.stark import site, StarkConfig, Option, get_choice_text
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django import forms
from django.db import transaction
from django.conf import settings


class CourseRecordConfig(StarkConfig):
    def display_title(self, row=None, header=False):
        if header:
            return "上课记录"
        tpl = "%s s%sday%s" %(row.class_obj.course.name,row.class_obj.semester,row.day_num,)
        return tpl

    def display_study_record(self, row=None, header=False):
        if header:
            return "学习记录"
        url = reverse('stark:crm_studyrecord_changelist')
        return mark_safe("<a href='%s?ccid=%s'>学习记录</a>" %(url,row.pk,))

    list_display = [display_title,display_study_record]

    def get_list_display(self):
        val = super().get_list_display()
        val.insert(0, StarkConfig.display_checkbox)
        return val

    def multi_init(self, request):
        """
        批量初始化
        :param request:
        :return:
        """
        id_list = request.POST.getlist('pk')  # [1,2]
        # 找到选中上课记录的班级
        # 找到班级下所有人
        # 为每个人生成一条学习记录
        for nid in id_list:
            record_obj = models.CourseRecord.objects.get(id=nid)
            stu_list = models.Student.objects.filter(class_list=record_obj.class_obj)

            exists = models.StudyRecord.objects.filter(course_record=record_obj).exists()
            if exists:
                continue

            study_record_list = []
            for stu in stu_list:
                study_record_list.append(models.StudyRecord(course_record=record_obj,student=stu))

            models.StudyRecord.objects.bulk_create(study_record_list)

    multi_init.text = "批量初始化"

    action_list = [multi_init,]