# -*-coding:utf-8 -*-
"""
@Time:2019/1/2 18:47
@Author:tzm
@Email:2234224472@qq.com
@File:views.py
"""
from flask import render_template, current_app, session, g, abort, request, jsonify
from info import constants, db
from info.models import News, User, Comment
from info.modules.news import news_blu

# 127.0.0.1/NEWS/1
from info.utils.common import user_login_data
from info.utils.response_code import RET


@news_blu.route("/news_comment", methods=["POST"])
def comment_news():
    """
    评论新闻或者回复某条新闻下制动的评论
    :return:
    """
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    news_id = request.json.get("news_id")
    comment_content = request.json.get("comment")
    parent_id = request.json.get("parent_id")

    # 2.判断参数
    if not all([news_id, comment_content]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")
    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")
        # 3.查询新闻并判断新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="数据查询错误")

    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到数据")
    # 3.初始化一个评论模型
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_content
    if parent_id:
        comment.parent_id = parent_id

    # 添加到数据库
    # 为什么要自己去commit（），因为在return的时候需要用到comment的id
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()

    return jsonify(errno=RET.OK, errmsg="OK", comment=comment.to_dict())


@news_blu.route("/news_collect", methods=["POST"])
@user_login_data
def collect_news():
    """
    收藏新闻
    1.接收参数
    2.判断参数
    3.查询新闻并判断新闻是否存在
    :return:
    """

    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登陆")

    # 1.接收参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    # 2.判断参数
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if action not in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 3.查询新闻并判断新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="数据查询错误")

    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到数据")

    # 4.收藏以及取消收藏
    if action == "cancel_collect":
        # 取消收藏
        if news in user.collection_news:
            user.collection_news.remove(news)
    else:
        if news not in user.collection_news:
            # 添加到用户的新闻收藏列表
            user.collection_news.append(news)

    return jsonify(errno=RET.OK, errmsg="操作错误")


@news_blu.route("/<int:news_id>")
@user_login_data
def news_detail(news_id):
    """新闻详情页信息"""
    # 查询用户登录信息
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
        news_dict_li.append(news.to_basic_dict())

    # 查询新闻数据
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
    if not news:
        # 报404错误，404错误统一显示页面后续在处理
        abort(404)

    # 更新新闻的点击次数
    news.clicks += 1

    is_collected = False
    if user:
        # 判断用户是否收藏当前新闻，如果收藏
        #  collection_news 后面可以不用加all，因为sqlalchemy会在使用的时候自动加载
        if news in user.collection_news:
            is_collected = True

    data = {
        "news_dict_li": news_dict_li,
        "user": user.to_dict() if user else None,
        "news": news.to_dict(),
        "is_collected": is_collected
    }
    return render_template("news/detail.html", data=data)
