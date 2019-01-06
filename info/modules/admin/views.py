# -*-coding:utf-8 -*-
"""
@Time:2019/1/5 21:13
@Author:tzm
@Email:2234224472@qq.com
@File:views.py
"""
from datetime import datetime, timedelta
import time
from flask import render_template, request, current_app, session, redirect, url_for, g
from info import constants
from info.models import User
from info.modules.admin import admin_blu
from info.utils.common import user_login_data


@admin_blu.route("/user_list")
def user_list():
    page = request.args.get("page", 1)

    # 判断参数
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    # 查询用户指定页数
    users = []
    total_page = 1
    current_page = 1

    try:
        paginate = User.query.filter(User.is_admin == False).order_by(User.create_time.desc()).paginate(page, constants.ADMIN_USER_PAGE_MAX_COUNT)
        users = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    # 进行模型列表转字典列表
    user_dict_li = []
    for user in users:
        user_dict_li.append(user.to_admin_dict())

    data = {
        "users": user_dict_li,
        "total_page": total_page,
        "current_page": current_page
    }

    return render_template("admin/user_list.html", data=data)


@admin_blu.route("/user_count")
def user_count():
    # 总人数
    total_count = 0
    try:
        total_count = User.query.filter(User.is_admin == False).count()
        print(total_count)
    except Exception as e:
        current_app.logger.error(e)
    # 月新增数
    mon_count = 0
    t = time.localtime()
    begin_mon_date = datetime.strptime(('%d-%02d-01' % (t.tm_year, t.tm_mon)), "%Y-%m-%d")
    try:
        mon_count = User.query.filter(User.is_admin == False, User.create_time > begin_mon_date).count()
    except Exception as e:
        current_app.logger.error(e)
    #
    day_count = 0
    begin_day_date = datetime.strptime(('%d-%02d-%02d' % (t.tm_year, t.tm_mon, t.tm_mday)), "%Y-%m-%d")
    try:
        day_count = User.query.filter(User.is_admin == False, User.create_time > begin_day_date).count()
    except Exception as e:
        current_app.logger.error(e)

    # 折线图数据
    active_count = []
    active_time = []

    today_date = datetime.strptime(('%d-%02d-%02d' % (t.tm_year, t.tm_mon, t.tm_mday)), "%Y-%m-%d")
    for i in range(0, 31):
        begin_date = today_date - timedelta(days=i)
        end_date = today_date - timedelta(days=(i - 1))
        count = User.query.filter(User.is_admin == False, User.last_login >= begin_date,
                                  User.last_login < end_date).count()
        active_count.append(count)
        active_time.append(begin_date.strftime('%Y-%m-%d'))

    # 数据翻转
    active_time.reverse()
    active_count.reverse()

    data = {
        "total_count": total_count,
        "mon_count": mon_count,
        "day_count": day_count,
        "active_count": active_count,
        "active_time": active_time
    }
    return render_template("admin/user_count.html", data=data)


@admin_blu.route("/index")
@user_login_data
def index():
    user = g.user
    return render_template("admin/index.html", user=user.to_dict())


@admin_blu.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # 判断当前是否有登陆，如果有登陆直接重定向到管理员后台主页
        user_id = session.get("user_id", None)
        is_admin = session.get("is_admin", False)
        if user_id and is_admin:
            return redirect(url_for("admin.index"))
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
