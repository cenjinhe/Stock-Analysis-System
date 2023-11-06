"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'user/', include('user.urls'), name='user'),
    # url别名反向解析,别名 name
    path(r'stockManage/', include('stock_manage.urls'), name='stockManage'),


]

"""
学习笔记
url(r'^index/$',views.index)是什么意思呢?
^匹配要检索的文本的开头,$匹配文本的结束
"""
