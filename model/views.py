from django.shortcuts import render_to_response, HttpResponse, redirect
from model import forms,models
import datetime

# 登陆页面
def login_view(request):
    if request.method == "POST":
        form = forms.login_form(request.POST)
        if form.is_valid():
            # 表单合法，则会把数据放在表单的cleaned_data中
            cd = form.cleaned_data
            username=cd['username']
            password=cd['password']
            try:
                user_db = models.User.objects.get(sno=username)#连接数据库检查密码正确性
                if user_db.pwd == password:
                    # 密码正确
                    request.session["sno"]=user_db.sno # 记录用户登陆状态
                    return redirect('/upload') # 登陆成功，跳转到/upload
                        # redirect 只能通过session传递参数
                else:
                    # 密码错误
                    return HttpResponse("password error or user dont exist")
            except models.User.DoesNotExist:
                # 用户不存在
                return HttpResponse("password error or user dont exist")
        else:
            # 表单不合法
            return HttpResponse("form invalid")
    else:
        form=forms.login_form()
        return render_to_response('login_form.html',{'form':form})

# 信息上传界面
def objUpload_view(request):
    if request.method=="POST":
        # 获取用户输入后的POST表单
        form=forms.objUpload_form(request.POST,request.FILES)# request.FILES是获取imagefield的要求，否则获取不到图片

        # 检查表单的合法性
        if form.is_valid():
            obj=models.Object()             # 创建上传的物品的对象
            try:
                user_db = models.User.objects.get(sno=request.session['sno']) #request.session通过cookie记录用户状态

                # 输入物品信息
                nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                obj.id = nowtime                            # 为物品生成一个当前时间的id，作为主键
                obj.name = form.cleaned_data['name']
                input_date = form.cleaned_data['time']
                obj.time = datetime.date(datetime.datetime.now().year,
                                         input_date.month,
                                         input_date.day)
                # 因为表单输入没有设置year（默认year=1900）需要重新设置
                # datetime 对象是不可修改的（not writable），实现赋值需要新的date对象
                obj.position = form.cleaned_data['position']
                obj.dscp = form.cleaned_data['dscp']
                obj.tag = form.cleaned_data['tag']
                obj.state = 0  # state=0 未审核状态
                obj.user = user_db
                if form.cleaned_data['img']:
                    # 如果有图片上传则执行以下部分
                    obj.img = form.cleaned_data['img']
                    obj.img.name = nowtime+".jpg"# 将图片名称修改为物品id

                obj.save()# 上传物品到数据库

                return HttpResponse("Upload successfully.")
            except models.User.DoesNotExist:
                # 用户不存在
                return HttpResponse("User dont exist.")
            except models.Object.DoesNotExist:
                # 物品信息没有存入数据库
                return HttpResponse("Upload error.")
        else:
            #表单不合法
            return HttpResponse("Input invalid.")
    else:
        # 处理非POST的情况,返回表单页面，用户输入数据
        if request.session['sno']:
            has_login = True
        else:
            has_login = False
        form = forms.objUpload_form
        context={}
        context['form']=form
        context['has_login']=has_login
        return render_to_response('objUpload.html',context)

# 信息显示页面
def info_view(request,obj_id):
    try:
        obj = models.Object.objects.get(id=obj_id) # 从Object表中获得要显示的物品信息
    except models.Object.DoesNotExist:
        return HttpResponse("Information dont exist:Object.")
    context = {}
    context['obj'] = obj
    if request.session['sno']:
        has_login = True
        context['user'] = obj.user
    else:
        has_login = False
    context['has_login']=has_login
    return render_to_response('info.html',context) # context包含:物品信息(obj)、信息发布用户信息(user)、访客是否登陆标记(has_login)