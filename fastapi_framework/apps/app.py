# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2022/01/07 17:26:26
@Author  :   sk 
@Version :   1.0
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from typing import Iterable
from fastapi import FastAPI, APIRouter


def _init_app_router(app: FastAPI, routers: Iterable[APIRouter] = None):
    if routers:
        for router in routers:
            app.include_router(router, prefix='/api')


def create_app(config: dict = None, routers: Iterable[APIRouter] = None):

    app = FastAPI()
    
    _init_app_router(app, routers)
    
    return app
