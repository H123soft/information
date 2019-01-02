# -*-coding:utf-8 -*-
"""
@Time:2019/1/2 18:45
@Author:tzm
@Email:2234224472@qq.com
@File:__init__.py.py
"""
# 新闻详情模块的蓝图
from flask import Blueprint

# 创建蓝图对象

news_blu = Blueprint("news", __name__, url_prefix="/news")

from . import views
