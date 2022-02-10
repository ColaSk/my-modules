# -*- encoding: utf-8 -*-
'''
@File    :   route.py
@Time    :   2022/02/10 11:00:48
@Author  :   sk 
@Version :   1.0
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from json import JSONDecodeError

from fastapi import Request
from fastapi.routing import APIRoute

from .log import logger


class MyRoute(APIRoute):
    """Extension Route and log request.json()"""

    def get_route_handler(self):
        
        original_route_handler = super().get_route_handler()

        async def log_request_detail(request: Request):

            logger.info('start request'.center(60, '*'))
            logger.info(f'{request.method} {request.url}')

            methods = ['POST', 'PUT', 'PATCH']
            content_type = request.headers.get('content-type', '')

            if request.method in methods and 'application/json' in content_type:
                try:
                    params = await request.json()
                    if params:
                        logger.info(params)
                except JSONDecodeError:
                    logger.error('encounter JSONDecodeError')
                except UnicodeDecodeError:
                    logger.error('encounter UnicodeDecodeError')
            logger.info('end request'.center(60, '*'))
            return await original_route_handler(request)

        return log_request_detail
