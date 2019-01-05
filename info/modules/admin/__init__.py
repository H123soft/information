# -*-coding:utf-8 -*-
"""
@Time:2019/1/5 21:12
@Author:tzm
@Email:2234224472@qq.com
@File:__init__.py.py
"""
from flask import Blueprint


admin_blu = Blueprint("admin",__name__)

from . import views

