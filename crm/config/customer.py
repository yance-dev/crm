from crm import models
from stark.service.stark import site, StarkConfig, Option, get_choice_text
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django import forms
from django.db import transaction
from django.conf import settings


class CustomerConfig(StarkConfig):

    def display_follow(self,row=None, header=False):
        if header:
            return '跟进记录'

        url = reverse("stark:crm_consultrecord_changelist")
        return mark_safe("<a href='%s?cid=%s'>跟进记录</a>" %(url,row.pk,))

    list_display = [
        'name',
        'qq',
        get_choice_text('status', '状态'),
        get_choice_text('gender', '性别'),
        get_choice_text('source', '来源'),
        display_follow

    ]

    order_by = ['-id', ]

    search_list = ['name', 'qq']

    list_filter = [
        Option('status', is_choice=True, text_func=lambda x: x[1]),
        Option('gender', is_choice=True, text_func=lambda x: x[1]),
        Option('source', is_choice=True, text_func=lambda x: x[1])
    ]



class PubModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', 'status']


class PublicCustomerConfig(StarkConfig):
    list_display = [
        'name',
        'qq',
        get_choice_text('status', '状态'),
        get_choice_text('gender', '性别'),
        get_choice_text('source', '来源')
    ]

    order_by = ['-id', ]

    search_list = ['name', 'qq']

    list_filter = [
        Option('gender', is_choice=True, text_func=lambda x: x[1]),
        Option('source', is_choice=True, text_func=lambda x: x[1])
    ]

    model_form_class = PubModelForm

    def multi_apply(self, request):
        """
        申请客户
        :param request:
        :return:
        """
        id_list = request.POST.getlist('pk')  # [1,2]
        current_user_id = 1  # 以后要改成去session中获取当前登陆用户ID

        my_customer_count = models.Customer.objects.filter(consultant_id=current_user_id, status=2).count()

        if (my_customer_count + len(id_list)) > settings.MAX_PRIVATE_CUSTOMER:
            return HttpResponse('做人别太贪心')

        flag = False
        with transaction.atomic():
            origin = models.Customer.objects.filter(id__in=id_list, consultant__isnull=True).select_for_update()
            if len(origin) == len(id_list):
                models.Customer.objects.filter(id__in=id_list).update(consultant_id=current_user_id)
                flag = True

        if not flag:
            return HttpResponse('已被其他顾问申请（手速太慢）')

    multi_apply.text = "申请客户"

    action_list = [multi_apply, ]

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_del)
        val.insert(0, StarkConfig.display_checkbox)
        return val

    def get_queryset(self):
        return self.model_class.objects.filter(consultant__isnull=True)




class PriModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', ]


class PrivateCustomerConfig(StarkConfig):
    def display_follow(self,row=None, header=False):
        if header:
            return '跟进记录'

        url = reverse("stark:crm_consultrecord_pri_changelist")
        return mark_safe("<a href='%s?cid=%s'>跟进记录</a>" %(url,row.pk,))

    list_display = [
        'name',
        'qq',
        get_choice_text('status', '状态'),
        get_choice_text('gender', '性别'),
        get_choice_text('source', '来源'),
        display_follow
    ]

    order_by = ['-id', ]

    search_list = ['name', 'qq']

    list_filter = [
        Option('status', is_choice=True, text_func=lambda x: x[1]),
        Option('gender', is_choice=True, text_func=lambda x: x[1]),
    ]

    model_form_class = PriModelForm

    def multi_remove(self, request):
        """
        申请客户
        :param request:
        :return:
        """
        id_list = request.POST.getlist('pk')  # [1,2]
        current_user_id = 1  # 以后要改成去session中获取当前登陆用户ID
        models.Customer.objects.filter(id__in=id_list, status=2, consultant_id=current_user_id).update(consultant=None)

    multi_remove.text = "移除客户"

    action_list = [multi_remove, ]

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_del)
        val.insert(0, StarkConfig.display_checkbox)
        return val

    def get_queryset(self):
        current_user_id = 1  # 以后要改成去session中获取当前登陆用户ID
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, form, modify=False):
        current_user_id = 1  # 以后要改成去session中获取当前登陆用户ID
        form.instance.consultant = models.UserInfo.objects.get(id=current_user_id)
        return form.save()
