from crm import models
from stark.service.stark import site, StarkConfig, Option, get_choice_text
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django import forms
from django.db import transaction
from django.conf import settings


class ConsultRecordConfig(StarkConfig):
    list_display = ['customer','note','consultant']

    def get_queryset(self):
        cid = self.request.GET.get('cid')
        if cid:
            return models.ConsultRecord.objects.filter(customer_id=cid)
        return models.ConsultRecord.objects


class PriModelForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ['customer','consultant']


class PriConsultRecordConfig(StarkConfig):
    list_display = ['customer','note','consultant']

    model_form_class = PriModelForm

    def get_queryset(self):
        cid = self.request.GET.get('cid')
        current_user_id = 1  # 以后要改成去session中获取当前登陆用户ID
        print(cid,current_user_id)
        if cid:
            return models.ConsultRecord.objects.filter(customer_id=cid,customer__consultant_id=current_user_id)
        return models.ConsultRecord.objects.filter(customer__consultant_id=current_user_id)

    def save(self,form,modify=False):
        if not modify:
            params = self.request.GET.get('_filter')
            cid,num = params.split('=',maxsplit=1)
            form.instance.customer = models.Customer.objects.get(id=num)
            current_user_id = 1
            form.instance.consultant =models.UserInfo.objects.get(id=current_user_id)

        form.save()