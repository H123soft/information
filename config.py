# -*-coding:utf-8 -*-
"""
@Time:2018/12/21 14:50
@Author:tzm
@Email:2234224472@qq.com
@File:config.py
"""
import logging
from redis import StrictRedis


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/information28?charset=utf8'
    SECRET_KEY = 'a random string'
    SQLALCHEMY_TRACK_MODIFCATIONS = False
    # 在请求结束时候，如果指定此配置为True  那么SQLChemy会自动执行一次db.session.commit()操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis 的配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # Session 保存配置
    SESSION_TYPE = 'redis'
    # 是否开启签名
    SESSION_USE_SIGNER = True

    # 设置过期时间
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

    # 设置过期时间
    SESSION_PERMANENT = False

    # 设置过期时间
    permanent_session_lifetime = 86400 * 2


    # 设置日志等级
    LOG_LEVEL= logging.DEBUG


class DevelopmentConfig(Config):
    """开发环境下的配置"""
    DEEBUG = True



class ProductionConfig(Config):
    """生产环境下的配置"""
    DEEBUG = False
    # 生产环境下的配置
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/infromtion?charset=utf8'
    LOG_LEVEL = logging.WARNING
class TestingConfig(Config):
    """单元测试环境下的配置"""
    DEBUG = True
    TESTING = True


config = {
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "testing": TestingConfig
}
    
