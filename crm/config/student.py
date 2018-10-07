from crm import models
from stark.service.stark import site, StarkConfig, Option, get_choice_text
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django import forms
from django.db import transaction
from django.conf import settings

class StudentConfig(StarkConfig):

    def display_class_list(self, row=None, header=False):
        if header:
            return "班级"
        class_list = row.class_list.all()
        class_name_list = [ "%s%s期" %(row.course.name,row.semester) for row in class_list]
        return ','.join(class_name_list)


    list_display = ['username','customer',display_class_list]

