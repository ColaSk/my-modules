# -*- encoding: utf-8 -*-
'''
@File    :   dbmodel.py
@Time    :   2021/12/29 10:13:20
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def init_db(app: Flask):

    db.init_app(app)
    Migrate(app, db)

    return app
