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
from typing import Callable, Dict, Iterable, Optional, Sequence
from fastapi import FastAPI, APIRouter, Depends


def _init_app_routers(app: FastAPI, routers: Iterable[APIRouter] = None) -> None:
    if not routers:
        return 

    for router in routers:
        app.include_router(router, prefix='/api')

def _init_app_exception_handlers(app: FastAPI, handlers: Dict[int, Callable] = None) -> None:
    if not handlers:
        return 
    
    for code, handler in handlers.items():
        app.add_exception_handler(code, handler)

def create_app(config: dict = None, 
               routers: Iterable[APIRouter] = None, 
               handlers: Iterable[Callable] = None,
               dependencies: Optional[Sequence[Depends]] = None) -> FastAPI:

    app = FastAPI(dependencies=dependencies)
    
    _init_app_routers(app, routers)
    _init_app_exception_handlers(app, handlers)

    return app
