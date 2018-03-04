#-*- coding: UTF-8 -*-

'''
主要是常用的工具函数
'''

from MarkDownBlog.config import *
import os

# 返回路径绝对，0代表不存在，1代表是文件, 第二个参数是文件的绝对路径，第三个参数是文件的相对目录路径
# ，2代表是目录，只接受相对路径
# p[0] 代表文件还是目录
# p[1] 代表绝对路径
# p[2] 相对目录
# p[3] 文件名称
def get_path(str_path):
    s = str_path.replace(ROOT_DIR, "")
    p = "/".join([ROOT_DIR, s])
    rel = ["", ""]

    if os.path.exists(p):
        if os.path.isfile(p):
            rel[0] = "file"
        elif os.path.isdir(p):
            rel[0] = "dir"
        rel[1] = p

    return rel 