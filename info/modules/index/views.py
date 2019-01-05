# -*-coding:utf-8 -*-
"""
@Time:2018/12/21 16:46
@Author:tzm
@Email:2234224472@qq.com
@File:views.py
"""
from flask import render_template, current_app, session, request, jsonify, g
from info import constants
from info.models import User, News, Category
from info.utils.common import user_login_data
from info.utils.response_code import RET

from . import index_blu


@index_blu.route("/news_list")
def news_list():
    """
    获取首页新闻数据
    """
    # 1.获取参数
    # 新闻的分类
    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")

    # 2.校验参数
    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数")

    filters = [News.status == 0]
    if cid != 1:  # 查询的不是最新的数据
        # 需要添加条件
        filters.append(News.category_id == cid)
    # 3.查询数据
    try:
        pageinate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询错误")

    # 取到当前页数据
    news_model_list = pageinate.items  # 模型对象列表
    total_page = pageinate.pages
    current_page = pageinate.page
    # 将模型对象列表转成字典列表
    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())

    data = {
        "total_page": total_page,
        "current_page": current_page,
        "news_dict_li": news_dict_li
    }
    return jsonify(errno=RET.OK, errmsg="OK", data=data)


@index_blu.route("/")
@user_login_data
def index():
    """
    显示首页
    1.如果用户已经登录，将当前登录用户的数据传到模板中，供模板显示
    2.
    :return:
    """
    # # 取到用户的id
    # # 显示用户是否登录的逻辑
    #
    # user_id = session.get("user_id", None)
    # user = None
    # if user_id:
    #     # 尝试查询用户的模型
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)
    user = g.user

    # 右侧的新闻排行的逻辑
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NGNWCEWS)
    except Exception as e:
        current_app.logger.error(e)
    # 定义一个空的字典列表，里面装 的就是字典
    news_dict_li = []
    # 遍历对象列表，将对象的字典添加到字典中
    for news in news_list:
        news_dict_li.append(news)

    # 查询分类数据，通过模板的形式渲染出来
    categories = Category.query.all()

    category_li = []
    for category in categories:
        category_li.append(category.to_dict())

    data = {
        "user": user.to_dict() if user else None,
        "news_dict_li": news_dict_li,
        "category_li": category_li
    }

    return render_template("news/index.html", data=data)


# 在浏览器网页打开的时候，浏览器会默认去请求更路径+favicon.icon下的小图标
# send_static_file 是flask去查找指定的静态文件所调用的方法

@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")
