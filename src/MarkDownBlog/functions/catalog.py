#-*- coding: UTF-8 -*-

'''
主要是对目录的操作
'''
from MarkDownBlog.config import *
from MarkDownBlog.functions.articles import *
from MarkDownBlog.functions.tools import *
from MarkDownBlog.tools.colorPrint import colorPrint

import math
import operator
import time
import threading

LOCK = threading.RLock()

# 线程组,刷新的目的是在添加了文章之后能够及时更新
THREADINGS = []
# 内存中保存的文章列表数量
ARTICLES_CACHE = []

# 获取某一路径下的文章缩略的描述字典
# {"num":2, visit_num:12, sort_by:time, des: True, path: /../, "articles":[{}, {}, {}]}
def get_a_new_articles_dict(str_path):
    ars = []
    ars = get_all_files_from_catalog(str_path)

    # 默认按时间排序，降序
    colorPrint.info('get all files from catalog and len %d' % len(ars))
    ars = sort_articles(ars, "time", True)
    colorPrint.info('after sort, len is %d' % len(ars))
    article_dict = {
        "num":len(ars),
        #访问数量，弹出依据
        "visit_num": 1,
        "sort_by": "time",
        # 是否排序，升序降序
        "des": True,
        "path": "".join(["/",str_path.strip("/")]),
        "articles": ars
    }

    return article_dict

# 缓存,输入路径，排序方式，升序降序
# 对ARTICLES_CACHE的操作,从 ARTICLES_CACHE中获得articles，返回的是按照指定的方式排序的文章列表
# [{} {} {} {} ...]
def get_articles_from_ARTICLES_CACHE(str_path, sort_by, des):
    articles = {}

    # 判断是否开启了线程
    # 判断线程是否开启了
    if len(THREADINGS) > 0:
        pass
    else:
        t = threading.Thread(target=refresh_thread, args=(REFRESH_TIME,))
        THREADINGS.append(t)
        t.setDaemon(True)
        t.start()

    l = len(ARTICLES_CACHE)
    colorPrint.info('get articles from articles cache, and articles cache has %d cache' %l)
    colorPrint.info('and path is ' + str_path)
    # 遍历，看看有没有已经存在的缓存
    for i in ARTICLES_CACHE:
        colorPrint.info('and the one has articles %d' %len(i['articles']))
        # 如果有的话,直接返回articles
        if i['path'].strip("/") == str_path.strip("/"):
            colorPrint.info('has same str path, and the cache has %d articles' %len(i['articles']))
            i['visit_num'] += 1

            # 判断是不是要求的排序方式
            if i["sort_by"] == sort_by and i["des"] == des:
                return i['articles']
            else:
                i["sort_by"] = sort_by
                i["des"] = des
                return sort_articles(i['articles'], i['isort_by'], i["des"])
    # 没有的话
    # 先判断tmp的大小，是否比设定的大,小的话添加进去
    if l < CACHE_SIZE:
        article_dict = get_a_new_articles_dict(str_path)
        if article_dict['sort_by'] == sort_by and article_dict["des"] == des:
            pass
        else:
            article_dict["sort_by"] == sort_by
            article_dict["des"] == des
            article_dict["articles"] = sort_articles(article_dict['articles'], article_dict['isort_by'], article_dict["des"])
        
        ARTICLES_CACHE.append(article_dict)
        return article_dict['articles']

    # 大于等于的话，弹出一个
    else:
        ARTICLES_CACHE.sort(key=lambda x: x['visit_num'], reverse=True)
        ARTICLES_CACHE.pop()
        article_dict = get_a_new_articles_dict(str_path)
        if article_dict['sort_by'] == sort_by and article_dict["des"] == des:
            pass
        else:
            article_dict["sort_by"] == sort_by
            article_dict["des"] == des
            article_dict["articles"] = sort_articles(article_dict['articles'], article_dict['sort_by'], article_dict["des"])
        ARTICLES_CACHE.append(article_dict)
        return article_dict['articles']

# 刷新ARTICLES_CACHE里面的文章
def refresh_articles_in_ARTICLES_CACHE():
    for i in ARTICLES_CACHE:
        i["articles"] = sort_articles(get_all_files_from_catalog(i["path"]), 
            i["sort_by"], i["des"])
        pass

# 开启一个线程专门刷新文章，最少10分钟刷新一次
def refresh_thread(t=10):
    sleep_t = 10
    if t > sleep_t:
        sleep_t = t
    while True:
        time.sleep(sleep_t*60)
        LOCK.acquire()
        print('sleep over 执行刷新！')
        refresh_articles_in_ARTICLES_CACHE()
        LOCK.release()
        pass

# 对文章进行排序,des为真是降序，为假为升序
# 输入[{}, {}, {}]
# 输出[{}, {}, {}, {}]
def sort_articles(articles, sort_by, des):
    if sort_by == "time":
        articles.sort(key=operator.itemgetter("ctime"), reverse=des)
    elif sort_by == "title":
        articles.sort(key=operator.itemgetter("title"), reverse=des)
    return articles

######################################################
# 获得某一目录下的文件，只要一层，不包括在config中已经忽略的内容
# 就是完整的带缩略内容的文件
# [{} {} {} {} {} {} {}]
def get_a_layer_file_from_catalog(str_path):
    p = get_path(str_path)
    fs = []

    if p[0] == "dir":
        article = {}
        lists = os.walk(p[1])
        for path, dirs, files in lists:
            for f in files:
                (name, file_type) = os.path.splitext(f)
                if name:
                    if name[0] not in IGNORE_PREFIX and \
                        name not in IGNORE_FILE and file_type in FILE_TYPE:
                        article = get_a_markdown_article_thumbnail(os.path.join(path, f))
                        fs.append(article)
            break

    return fs

# 得到某一目录下的所有文件缩略
# 返回[{} {} {} {} ...]
def get_all_files_from_catalog(str_path):
    fs = []
    p = get_path(str_path)

    if p[0] == "dir":
        lists = os.walk(p[1])
        for path, dirs, files in lists:
            path_name = path.replace(ROOT_DIR, '').split('/')
            r = True
            for i in path_name:
                if i:
                    if i in IGNORE_DIR or i[0] in IGNORE_PREFIX:
                        r = False
                        break
            if r:
                for f in files:
                    article = {}
                    (name, file_type) = os.path.splitext(f)
                    if name[0] not in IGNORE_PREFIX and \
                        name not in IGNORE_FILE and file_type in FILE_TYPE:
                        f_path = os.path.join(path, f)
                        article = get_a_markdown_article_thumbnail(f_path)

                        fs.append(article)

    return fs

# 获得某一目录下的目录，只要一层目录
def get_a_layer_dir_from_catalog(str_path):
    p = get_path(str_path)
    ds = []
    a_dir = {}

    if p[0] == "dir":
        for d in os.listdir(p[1]):
            d_path = os.path.join(p[1], d)
            if os.path.isdir(d_path):
                if d not in IGNORE_DIR and d[0] not in IGNORE_PREFIX:
                    a_dir['name'] = d
                    a_dir['path'] = d_path.replace(ROOT_DIR, "")

                    ds.append(a_dir)

    return ds

# 得到目录结构
def get_dir_structure(str_path):
    ds = []
    p = get_path(str_path)

    if p[0] == "dir":
        for d in os.listdir(p[1]):
            d_path = os.path.join(p[1], d)
            if not os.path.isdir(d_path):
                continue
            if d[0] not in IGNORE_PREFIX and d not in IGNORE_DIR:
                os_stat = os.stat(d_path)
                a_d = {}
                a_d['name'] = d
                a_d['mtime'] = os_stat.st_mtime
                a_d['path'] = os.path.join(str_path, d)
                a_d['children'] = []

                a_d['children'] += get_dir_structure(os.path.join(str_path, d))

                ds.append(a_d)
    return ds

# 得到分页文章列表，输入某一个路径，以及第几页, 排序方式，降序升序,页大小，返回属于该路径下的所有的文章列表
# 返回请求页的我文章列表，分了多少页，当前是第几页，是否成功
# {success: , all_pages_num: , current_page_num: , articles:[{} {} {} {}]}
def get_page_articles(str_path, page_num, sort_by, des, page_size):
    response_json = {}
    # response_json的默认值
    success = False
    all_pages_num = 1
    articles_list = []

    # 首先看看有没有路径，没有的话直接返回错误，有的话如果
    # 其他参数有空的那么使用默认参数
    if str_path:
        colorPrint.info('get page articles and has path ' + str_path)
        success = True

        # 再次确认设置页数 排序方式 每页大小值
        if not page_num:
            page_num = 1
        if not sort_by:
            sort_by = SORT_BY
        if not page_size:
            page_size = DEFAULT_ENTRY_NUM
        if des != True and des != False:
            des = DEFAULT_DES

        # 得到str_path下所有文章的列表[{} {} {} {}...]
        # 判断是不是需要缓存
        if REFRESH_TIME > 0:
            articles_list = get_articles_from_ARTICLES_CACHE(str_path, sort_by, des)
            colorPrint.info('get articles from cache and articles %d' %len(articles_list))
        else:
            articles_list = get_all_files_from_catalog(str_path)
            articles_list = sort_articles(articles_list, sort_by, des)

        all_articles_num = len(articles_list)

        # 如果有文章的话
        if all_articles_num:
            colorPrint.info('has articles!!')
            # 获取页数
            all_pages_num = math.ceil(all_articles_num/page_size)
            colorPrint.info('pages %d' %all_pages_num)
            # 第几页
            if page_num < 1:
                page_num = 1
            elif page_num > all_pages_num:
                page_num = all_pages_num
            # 获取第几页
            articles_list = articles_list[((int(page_num)-1)*int(page_size)) : (int(page_num)*int(page_size))]
            colorPrint.info('length of articles list %d' % len(articles_list))
    response_json["success"] = success
    response_json["all_pages_num"] = all_pages_num
    response_json["current_page_num"] = page_num
    response_json["articles"] = articles_list

    return response_json

# 获得最新的前几篇文章，包括缩略,传入获得的数量，然后返回
# [{}, {}, {}, {}]
def newest_article(num):
    articles = get_articles_from_ARTICLES_CACHE("/", "time", True)
    articles = sort_articles(articles, "time", True)

    return articles[0:num]
