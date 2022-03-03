# -*- encoding: utf-8 -*-
'''
@File    :   middleware.py
@Time    :   2022/01/20 17:49:03
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from fastapi import Request


async def before_request(request: Request, call_next):
    
    # ! 异步获取request信息会被阻塞
    # print(await request.json())

    return await call_next(request)