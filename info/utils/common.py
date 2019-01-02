# -*-coding:utf-8 -*-
"""
@Time:2018/12/30 21:35
@Author:tzm
@Email:2234224472@qq.com
@File:common.py
"""
import functools
# 公用的自定义工具类
from flask import session, current_app, g
from info.models import User


def to_index_class(index):
    """返回指定索引对应的类名"""
    if index == 0:
        return "first"
    elif index == 1:
        return "second"
    elif index == 2:
        return "third"

    return " "


def user_login_data(f):
    # 使用functools.wraps去装饰内层函数，可以保持当前装饰去装饰的函数的__name__的值不变
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        user_id = session.get("user_id", None)
        user = None
        if user_id:
            # 尝试查询用户的模型
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        g.user= user
        return f(*args,**kwargs)
    return wrapper


# def query_user_data():
#     user_id = session.get("user_id", None)
#     user = None
#     if user_id:
#         # 尝试查询用户的模型
#         try:
#             user = User.query.get(user_id)
#         except Exception as e:
#             current_app.logger.error(e)
#
#         return user
#     return None
    
    
    
