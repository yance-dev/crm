from django.shortcuts import render,redirect
from crm import models
from rbac.service.init_permission import init_permission
def login(request):
    if request.method == "GET":
        return render(request,'login.html')

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    user_obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
    if not user_obj:
        return render(request, 'login.html',{'msg':'用户名或密码错误'})

    # 用户名和密码正确,用户信息放入session
    request.session['user_info'] = {'id':user_obj.id,'name':user_obj.name}

    # 权限信息初始化
    init_permission(user_obj,request)

    return redirect('/stark/crm/course/list/')
