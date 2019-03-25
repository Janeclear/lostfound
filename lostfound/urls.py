"""lostfound URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from model.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login$',login_view),# 登陆界面
    url(r'^upload$',objUpload_view), # 物品信息上传
    url(r'^info/(?P<obj_id>\d+)$',info_view), # 信息展示页面：(\d+)接收一个变量，是“物品”的id，视图函数通过识别这个变量去数据库找到对应的物品记录
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# 显示图片的需要（参考https://blog.csdn.net/c_beautiful/article/details/79755368
