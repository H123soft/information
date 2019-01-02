# -*-coding:utf-8 -*-
"""
@Time:2019/1/2 18:47
@Author:tzm
@Email:2234224472@qq.com
@File:views.py
"""
from flask import render_template, current_app, session, g, abort
from info import constants
from info.models import News, User
from info.modules.news import news_blu

# 127.0.0.1/NEWS/1
from info.utils.common import user_login_data


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
        "is_collected":is_collected
    }
    return render_template("news/detail.html", data=data)