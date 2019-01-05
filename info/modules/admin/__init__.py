# -*-coding:utf-8 -*-
"""
@Time:2019/1/5 21:12
@Author:tzm
@Email:2234224472@qq.com
@File:__init__.py.py
"""
from flask import Blueprint, session, redirect, request, url_for

admin_blu = Blueprint("admin", __name__)

from . import views


@admin_blu.before_request
def check_admin():
    is_admin = session.get("is_admin", False)
    if not is_admin and not request.url.endswith(url_for("admin.login")):
        return redirect("/")
