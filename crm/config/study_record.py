from crm import models
from stark.service.stark import site, StarkConfig, Option, get_choice_text
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse
from django import forms
from django.forms import modelformset_factory
from django.db import transaction
from django.conf import settings


class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['student','record','score','homework_note']

class StudyRecordConfig(StarkConfig):

    def get_urls(self):
        urlpatterns = [
            url(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
        ]
        return urlpatterns


    def changelist_view(self,request):
        ccid = request.GET.get('ccid')
        model_formset_cls = modelformset_factory(models.StudyRecord,StudyRecordModelForm,extra=0)
        queryset = models.StudyRecord.objects.filter(course_record_id=ccid)
        if request.method == "GET":
            formset = model_formset_cls(queryset=queryset)
            return render(request,'study_record.html',{'formset':formset})

        formset = model_formset_cls(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/stark/crm/studyrecord/list/?ccid=%s' %ccid )
        return render(request, 'study_record.html', {'formset': formset})