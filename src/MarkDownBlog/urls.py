"""MarkDownBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import MarkDownBlog.blog.views as blog
import MarkDownBlog.blog.interface as blog_interface

# 页面
urlpatterns = [
    url(r"^(?P<page>\d*)$", blog.home),
    url(r'^sheji/(?P<page>\d*)$', blog.sheji),
    url(r'^sheying/(?P<page>\d*)$', blog.sheying),
    url(r'^suibi/(?P<page>\d*)$', blog.suibi),
    url(r'^project/(?P<page>\d*)$', blog.xiangmu),
    url(r'^biji/(?P<page>\d*)$', blog.biji),
    url(r'^contact$', blog.contact),
    url(r'^readArticle/(?P<file_path>.*)(?P<file_type>\.*\..*?).html/$', blog.readArticle),
] 

# 接口,废弃
urlpatterns += [
    url(r'^getArticles/$', blog_interface.getArticles),
    url(r'^getAnArticle/$', blog_interface.getAnArticle),
    url(r'^emailToMe/$', blog.email_to_me),
]