#coding:utf-8

##############################
# 还需要的功能，
# 根据用户配置的模块以及模式，自动设置，不需要更改views代码
# 添加用户评论功能，评论之后邮件通知
# 添加定时刷新功能
# 添加后台功能
#   添加后台添加文章功能
#   添加数据保存到云盘
#   添加后台进行用户配置功能

###########系统设置#############
# 默认缓存数量
CACHE_SIZE = 10
# 刷新时间，单位分钟，小于0等于0代表不使用缓存，同时CACHE_SIZE无效，默认10分钟，可以比10大，比10小默认为10
REFRESH_TIME = 20

###########博客设置#############
# 博客根目录
ROOT_DIR = "/home/ever/Documents/blog/"
# 每页默认显示条目数量
DEFAULT_ENTRY_NUM = 6
# 默认排序方法
SORT_BY = 'time'
# 默认降序
DEFAULT_DES = True
# 忽略前缀，包括文件和文件名
IGNORE_PREFIX = ['.', '_', '*', '~']
# 忽略文件夹名称
IGNORE_DIR = ['img', 'file', 'code', 'media', 'test', 'tmp', 'src']
# 忽略的文件名称
IGNORE_FILE = ['临时', 'tmp']
# 允许读取的文件后缀
FILE_TYPE = ['.md', '.markdown', '.html']

###########网页设置############
# 模板主题
THEME = 'blackAndWhite'
# 主题顶栏设置
# 包括大标题，小标题，显示的模块名称，模块后面应该跟着链接，同时应该有模块的模式，比如三列，两列，一列等等模式
TOP_BAR = {
    "title": "城南旧事",
    "list": [
        {"首页": ""},
        {"笔记": "biji"},
        {"随笔": "suibi"},
        {"设计": "sheji"},
        {"摄影": "sheying"},
        {"作品": "project"},
        {"联系": "contact"}
    ]
}
# 缩略显示文件的前几行
SHOW_LINES = 15

# 需不需要过滤缩展示页的图片，一般ARTICLE_DEFAULT的top_icon为空的时候设置
# 意思是如果文章前几行有图片的话，那么就会显示
# 一般不显示，而是在模板中使用icon
SHOW_ARTICLE_IMG_IN_THUMBNAIL = False

###########个人信息设置############
AUTHOR_INFO = {
    "name": "redusty",
    "icon": [""],
    "des": [""],
    "qrcode": [""],
    "address": [""],
    "phone": [""],
    "email":[""],
    "qq": [""],
    "hobby":[""],
    "moto": "The quiter you become, the more you are able to hear.",
    "introduceYourself": "",
}

###########默认文章信息设置############
ARTICLE_DEFAULT = {
    "source": "原创",
    # 默认缩略图图标
    "icon": "/static/img/logo2.jpg",
    # 文章顶部图片
    "top_icon": "",
}

###########默认游客信息#############
GUEST_INFO = {
    "name" : "guest",
    "avatar" : "",
    "des" : ""
}

###########邮件配置###########
EMAIL = {
    # 邮件服务器
    "host": "smtp.163.com",
    # 邮件服务器端口
    "port": 25,
    # 邮箱名称
    "user": "binary@163.com",
    # 邮箱密码
    "password": "tian163",
    # 接收邮件的人
    "emailto": ["redusty@163.com",]
}
