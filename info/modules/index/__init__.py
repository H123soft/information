# -*-coding:utf-8 -*-
"""
@Time:2018/12/21 16:14
@Author:tzm
@Email:2234224472@qq.com
@File:__init__.py.py
"""
from flask import Blueprint


index_blu = Blueprint("index",__name__,)

from . import views

