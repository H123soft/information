# -*-coding:utf-8 -*-
"""
@Time:2019/1/5 21:13
@Author:tzm
@Email:2234224472@qq.com
@File:views.py
"""
from flask import render_template, request, current_app, session, redirect, url_for
from info.models import User
from info.modules.admin import admin_blu

@admin_blu.route("/index")
def index():
    return render_template("admin/index.html")


@admin_blu.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GRT":
        return render_template("admin/login.html")

    # 获取登录参数
    username = request.form.get("username")
    password = request.form.get("password")

    # 判断参数
    if not all([username, password]):
        return render_template("admin/login.html", errmsg="参数错误")

    # 查询当前用户
    try:
        user = User.query.filter(User.mobile == username, User.is_admin == True).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/login.html", errmsg="用户信息查询失败")
    if not user:
        return render_template("admin/login.html", errmsg="未查询到用户信息")

    # 校验密码
    if not user.check_passowrd(password):
        return render_template("admin/login.html", errmsg="用户名或密码错误")

    # 保存用户的信息
    session["user_id"] = user.id
    session["moblie"] = user.mobile
    session["nick_name"] = user.nick_name
    session["is_admin"] = user.is_admin

    #  跳转页面
    return redirect(url_for("admin.index"))
