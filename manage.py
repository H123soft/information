# -*-coding:utf-8 -*-
"""
@Time:2018/12/20 21:07
@Author:tzm
@Email:2234224472@qq.com
@File:manage.py
"""

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from info import create_app,db,models




# 通过指定的配置名字创建对应配置的app
# creat_app就类似与工厂方法
app = create_app("development")

manager = Manager(app)

# 将app与db关联
Migrate(app,db)

# 将迁移命令添加到manager中
manager.add_command('db',MigrateCommand)








if __name__ == '__main__':
    print(app.url_map)
    manager.run()