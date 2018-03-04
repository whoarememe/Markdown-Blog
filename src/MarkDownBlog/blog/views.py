#coding:utf-8
# 视图文件
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
# 邮件
from django.core.mail import send_mail
from django.template import RequestContext
from MarkDownBlog.functions.articles import *
from MarkDownBlog.functions.catalog import *
import time


# 阅读文章
def readArticle(request, file_path, file_type):
    print("i will read")
    print(file_type + " path " + file_path)
    article = {}
    for i in file_path.split("/"):
        print("i am i ===> " + i)
        if i in IGNORE_DIR or i in IGNORE_FILE \
            or i[0] in IGNORE_PREFIX:
            return render(request, "readArticle.html", {
                "article": article,
                "top_bar": TOP_BAR
            })

    if file_type in FILE_TYPE:
        print("o i am here")
        article = get_a_markdown_article("".join([file_path, file_type]))
    return render_to_response("readArticle.html", {
        "article": article,
        "top_bar": TOP_BAR
    })


# test
def test(request):
    return render_to_response("base.html")


# home
def home(request, page):
    rel = {}
    if not page:
        page = 1

    rel = get_page_articles("/", int(page), "", "", "")
    if rel["success"]:
        return render_to_response(
            "articleList.html", {
                "articles": rel["articles"],
                "all_pages_num": rel["all_pages_num"],
                "current_page_num": rel["current_page_num"],
                "top_bar": TOP_BAR
            })


# 摄影
def sheying(request, page):
    rel = {}
    if not page:
        page = 1

    rel = get_page_articles("/摄影", int(page), "", "", "")
    if rel["success"]:
        return render_to_response(
            "articleList.html", {
                "articles": rel["articles"],
                "all_pages_num": rel["all_pages_num"],
                "current_page_num": rel["current_page_num"],
                "top_bar": TOP_BAR
            })


# 设计
def sheji(request, page):
    rel = {}
    if not page:
        page = 1

    rel = get_page_articles("/设计", int(page), "", True, "")
    if rel["success"]:
        return render_to_response(
            "articleList.html", {
                "articles": rel["articles"],
                "all_pages_num": rel["all_pages_num"],
                "current_page_num": rel["current_page_num"],
                "top_bar": TOP_BAR
            })


# 随笔
def suibi(request, page):
    rel = {}
    if not page:
        page = 1

    rel = get_page_articles("/随笔", int(page), "", True, "")
    if rel["success"]:
        return render_to_response(
            "articleList.html", {
                "articles": rel["articles"],
                "all_pages_num": rel["all_pages_num"],
                "current_page_num": rel["current_page_num"],
                "top_bar": TOP_BAR
            })


# 笔记
def biji(request, page):
    rel = {}
    if not page:
        page = 1

    rel = get_page_articles("/笔记", int(page), "", True, "")
    if rel["success"]:
        return render_to_response(
            "articleList.html", {
                "articles": rel["articles"],
                "all_pages_num": rel["all_pages_num"],
                "current_page_num": rel["current_page_num"],
                "top_bar": TOP_BAR
            })


# 项目
def xiangmu(request, page):
    rel = {}
    if not page:
        page = 1

    rel = get_page_articles("/小东西", int(page), "", True, "")
    if rel["success"]:
        return render_to_response(
            "articleList.html", {
                "articles": rel["articles"],
                "all_pages_num": rel["all_pages_num"],
                "current_page_num": rel["current_page_num"],
                "top_bar": TOP_BAR
            })


# 联系
def contact(request):
    return render_to_response("contact.html", {"top_bar": TOP_BAR})


def email_to_me(request):
    errors = {}
    if request.method == "POST":
        if not request.POST.get("name", ""):
            errors["name"] = "please enter a name"
        if not request.POST.get("subject", ""):
            errors["subject"] = 'Enter a subject'
        if not request.POST.get('message', ''):
            errors["message"] = 'Enter a message'
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors["email"] = 'Enter a right email'

        if not errors:
            send_mail(
                request.POST['subject'],
                "mail from:" + request.POST.get('email') + "\n" +
                request.POST['message'],
                EMAIL["user"],
                EMAIL["emailto"],
            )

        return HttpResponseRedirect('www.baidu.com')
