# -*- encoding: utf-8 -*-
'''
@File    :   application.py
@Time    :   2022/01/07 17:26:26
@Author  :   sk 
@Version :   1.0
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from typing import Callable, Dict, Iterable, Optional, Sequence
from fastapi import FastAPI, APIRouter, Depends
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

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

def _init_app_middleware(app: FastAPI, middlewares: Optional[Sequence[Callable]] = None) -> None:
    if not middlewares:
        return

    for middleware in middlewares:
        app.add_middleware(BaseHTTPMiddleware, dispatch=middleware)

    # app.middleware()


def create_app(config: dict = None, 
               routers: Iterable[APIRouter] = None, 
               handlers: Iterable[Callable] = None,
               dependencies: Optional[Sequence[Depends]] = None,
               middlewares: Optional[Sequence[Callable]] = None) -> FastAPI:

    app = FastAPI(dependencies=dependencies)
    
    _init_app_routers(app, routers)
    _init_app_exception_handlers(app, handlers)
    _init_app_middleware(app, middlewares)

    return app
