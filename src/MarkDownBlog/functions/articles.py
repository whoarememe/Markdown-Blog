#-*- coding: UTF-8 -*-

'''
主要是对文章的操作函数
'''

from MarkDownBlog.config import AUTHOR_INFO, ARTICLE_DEFAULT
from MarkDownBlog.settings import STATIC_URL
from MarkDownBlog.functions.tools import *
import os
import json
import sys
import re
import markdown
import time

# 得到一篇文章完整内容,同时是正则替换之后的
def get_an_article(str_path):
    p = get_path(str_path)
    article = {}
    print(" i will panduan is file====>" + str_path)
    # 如果是文件，那么返回
    if p[0] == "file":
        print("i am file, i will read====>" + str_path)
        stat_info = os.stat(p[1])
        mtime = stat_info.st_mtime
        ctime = stat_info.st_ctime
        (f_title, f_type) = os.path.splitext(p[1].strip("/").split("/")[-1])
        f_path = p[1].replace(ROOT_DIR, "")

        article["title"] = f_title
        article["author"] = AUTHOR_INFO["name"]
        article["type"] = f_type
        article["mtime"] = mtime
        article["ctime"] = ctime
        article["str_ctime"] = time.strftime("%Y-%m-%d", time.localtime(ctime))
        article["path"] = f_path.strip('/')
        # 缩略展示图标
        article["icon"] = ARTICLE_DEFAULT["icon"]
        # 文章头部图标
        article["top_icon"] = ARTICLE_DEFAULT["top_icon"]
        # 文章来源原创还是转载
        article["source"] = ARTICLE_DEFAULT["source"]
        # 标签
        article["label"] = []
        article["love"] = 0
        article["comments"] = 0
        article["content"] = ""

        content = ""
        f = open(p[1])
        try:
            first_line = f.readline()
            content = f.read()

            try:
                dict_first_line = json.loads(first_line, encoding='utf-8')
                article = dict(article, **dict_first_line)
            except ValueError:
                content = "".join([first_line, content])
        except:
            info = sys.exc_info()  
            print(info[0],":",info[1])
        finally:
            f.close()

        article["content"] = replace_content(content, str_path)
    else:
        article["content"] = ""
    return article


# 获得markdown解析后的文章
def get_a_markdown_article(str_path):
    article = {}

    article = get_an_article(str_path)
    article['content'] = markdown.markdown(article["content"], ['extra', 'codehilite'])

    return article

# 获得前几行的缩略视图
def get_an_article_thumbnail(str_path):
    p = get_path(str_path)
    article = {}

    # 如果是文件，那么返回
    if p[0] == "file":
        stat_info = os.stat(p[1])
        mtime = stat_info.st_mtime
        ctime = stat_info.st_ctime
        (f_title, f_type) = os.path.splitext(p[1].strip("/").split("/")[-1])
        f_path = p[1].replace(ROOT_DIR, "")

        article["title"] = f_title
        article["author"] = AUTHOR_INFO["name"]
        article["type"] = f_type
        article["mtime"] = mtime
        article["ctime"] = ctime
        article["str_ctime"] = time.strftime("%Y-%m-%d", time.localtime(ctime))
        article["path"] = f_path.strip("/")
        # 缩略展示图标
        article["icon"] = ARTICLE_DEFAULT["icon"]
        # 文章头部图标
        article["top_icon"] = ""
        # 文章来源原创还是转载
        article["source"] = ARTICLE_DEFAULT["source"]
        # 标签
        article["label"] = []
        article["love"] = 0
        article["comments"] = 0
        article["content"] = ""

        content = ""
        f = open(p[1])
        try:
            first_line = f.readline()
            # 获得前几行
            content = "".join(f.readlines()[0:SHOW_LINES])

            try:
                dict_first_line = json.loads(first_line, encoding='utf-8')

                article = dict(article, **dict_first_line)
            except ValueError:
                content = "".join([first_line, content])
        except:
            info=sys.exc_info() 
            print(info[0],":",info[1])
        finally:
            f.close()

        if SHOW_ARTICLE_IMG_IN_THUMBNAIL:
            article["content"] = replace_content(content, str_path)
        else:
            article["content"] = replace_null(content)

        return article

# 得到文章的缩略，但是文章内容是markdown转换之后的
def get_a_markdown_article_thumbnail(str_path):
    article = get_an_article_thumbnail(str_path)
    if article['type'] == '.md':
        article["content"] = markdown.markdown(article["content"])

    return article

# 将图片或者文件替换为静态路径
def replace_content(content, str_path):
    # 匹配链接文件
    # 只匹配开头是.和..连接文件，也就是相对于当前文件路径的路径，http,/，什么的不匹配
    s = '\[(.*)\]\((\.{1,2})(.*)\)'
    p = re.compile(s)

    rel = re.sub(p, '[\\1]('+ STATIC_URL + '/' +\
        os.path.split(str_path.replace(ROOT_DIR, ""))[0]\
        + '/' +'\\2' + '\\3)', content)

    return rel

# 将图片以及链接图片替换为空
def replace_null(content):
    s = '!\[.*\]\(.*\)'
    p = re.compile(s)

    rel = re.sub(p, '', content)

    return rel