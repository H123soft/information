# -*-coding:utf-8 -*-
"""
@Time:2018/12/30 21:35
@Author:tzm
@Email:2234224472@qq.com
@File:common.py
"""


# 公用的自定义工具类

def to_index_class(index):
    """返回指定索引对应的类名"""
    if index == 0:
        return "first"
    elif index == 1:
        return "second"
    elif index == 2:
        return "third"

    return " "
