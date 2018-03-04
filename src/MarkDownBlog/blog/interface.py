#-*- coding: UTF-8 -*-

'''
实现一些接口，用于前台的访问
'''

from MarkDownBlog.functions.catalog import *
from MarkDownBlog.functions.articles import *
from django.http import HttpResponse
from django.http import JsonResponse

import json
import math
import markdown

# 表示此页已废弃，打算使用静态页面，直接查看views.py

# @interface
# 得到文章列表
def getArticles(request):
    response_json = {}
    success = True
    articles = []
    # 总的页数
    pages = 1
    paging = True
    level = 'one'
    # 第几页
    page_num = 1
    page_size = DEFAULT_ENTRY_NUM
    path = ""
    sort_by = 'time'
    msg = "未知错误"

    if request.method == 'POST':
        print("i am post")
        # 路径
        path = request.POST.get("path", "")
        print("这是路径这是路径" + path)
        # 先判断有没有路径
        if path:
            print("i have path")
            # 判断paging为真代表分页，为假代表不分页, 默认分页
            paging = request.POST.get("paging", True)
            # 得到层次，是所有的还是一层,默认一层
            level = request.POST.get("level", 'one')
            # 默认第一页
            page_num = request.POST.get("pageNum", 1)
            if page_num == 0:
                page_num = 1
            # 每页数量，默认为配置文件中的数量
            page_size = request.POST.get("page_size", DEFAULT_ENTRY_NUM)
            # 排序方法，默认为时间
            sort_by = request.POST.get("sortBy", SORT_BY)

            # 在判断层次
            # 所有内容
            if level == 'all':
                print(" i am all")
                articles = get_articles_from_tmp_articles(path)
            # 其他情况是一层
            else:
                print("i am one")
                articles = get_a_layer_file_from_catalog(path)
            
            # 计算长度用于分页
            l = len(articles)
            print("要获得第" + page_num + "页")
            # 有文章
            if l:
                print("i have articles")
                success = True
                # 分页总数
                pages = math.ceil(l/page_size)
                # 如果分页
                if paging:
                    print("i am paging")
                    articles = articles[((int(page_num)-1)*int(page_size)) : (int(page_num)*int(page_size))]
                # 如果不分页
                else:
                    paging = False
                    pass
            # 没文章
            else:
                success = False
                msg = "没有文章"
        # 没路径
        else:
            success = False
            msg = "路径错误"
    # 不是post
    else:
        success = False
        msg = "not post"
    print(request.method)
    if success:
        print("i am success")
        response_json['success'] = success
        response_json['level'] = level
        response_json['pageNum'] = page_num
        response_json['pageSize'] = page_size
        response_json['sortBy'] = sort_by
        response_json['path'] = path
        response_json['articles'] = articles
        response_json['paging'] = paging
        response_json['pages'] = pages
    else:
        print("i am failed")
        response_json['success'] = success
        response_json['msg'] = msg

    return JsonResponse(response_json)

# @interface
# 得到一篇文章
def getAnArticle(request):
    print("i am in get an article")
    response_json = {}
    success = False
    article = {}

    if request.method == 'POST':
        print("i will get path")
        path = request.POST.get('path', '')
        print("article path is " + path)
        if path:
            success = True
            article = get_an_article(path)
        else:
            success = False
    else:
        success = False

    if success:
        response_json['success'] = success
        response_json['article'] = article
    else:
        response_json['success'] = success
        response_json['msg'] = ''

    return JsonResponse(response_json)

# @interface
# 得到html转码后的文章
def getAnArticleHtml(request):
    response_json = {}
    success = False
    article = {}

    if request.method == 'POST':
        path = request.POST.get('path', '')
        if path:
            success = True
            article = get_an_article(path)
        else:
            success = False
    else:
        success = False

    if success:
        response_json['success'] = success
        response_json['article'] = markdown.markdown(article)
    else:
        response_json['success'] = success
        response_json['msg'] = ''

    return JsonResponse(response_json)

# @interface
# 得到目录结构
def get_catalog_structure(request):
    response_json = {}
    success = True
    catalog = []
    path = ""

    if request.method is 'POST':
        path = request.POST.get('path', "")
        if path:
            success = True
            catalog = get_dir_structure(path)
        else:
            success = False
    else:
        success = False
    
    if success:
        response_json['path'] = path
        response_json['success'] = success
        response_json['catalog'] = catalog
    else:
        response_json['success'] = success
        response_json['msg'] = ''

    return JsonResponse(response_json)

# @interface
# 得到一层目录
def get_catalog(request):
    response_json = {}
    success = True
    catalog = []
    path = ""

    if request.method is 'POST':
        path = request.POST.get('path', "")
        if path:
            success = True
            catalog = get_a_layer_dir_from_catalog(path)
        else:
            success = False
    else:
        success = False

    if success:
        response_json['path'] = path
        response_json['success'] = success
        response_json['catalog'] = catalog
    else:
        response_json['success'] = success
        response_json['msg'] = ''

    return JsonResponse(response_json)

def test(request):
    response_json = {}
    
    response_json['success'] = True
    response_json['article'] = get_articles_from_tmp_articles("/")[1:10]

    # re = {}
    # re['method'] == 'POST'
    # re['path'] = '/'
    # re['level'] = 'all'

    # response_json['all'] = getArticles(re)

    return JsonResponse(response_json)
    