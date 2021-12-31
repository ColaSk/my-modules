# -*- encoding: utf-8 -*-
'''
@File    :   rpc_wrapper.py
@Time    :   2021/12/31 10:14:40
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import logging
from functools import wraps
from nameko.rpc import rpc as nameko_rpc
from .response import RpcErrorResponse, RpcSuccessResponse

logger = logging.getLogger(__name__)

def rpc(func):
    """
    Nameko Rpc Dispatch Result Wrapper
    rpc 请求结果包装器, 将nameko rpc进行封装添加装饰器, 统一进行response 处理
    TODO: 定义各种服务异常
    """
    @wraps(func)
    @nameko_rpc
    def wrapper(*args, **kwargs):
        try:
            call_result = func(*args, **kwargs)
        except Exception as e:
            ex_msg = e.msg if hasattr(e, 'msg') else e.__str__()
            code = e.code if hasattr(e, 'code') else -1
            status_code = e.code if hasattr(e, 'status_code') else -1
            logger.error(f'ex_msg: {ex_msg}, code: {code}, status_code: {status_code}')
            return RpcErrorResponse(status_code=status_code, msg=ex_msg, code=code)()
        
        return RpcSuccessResponse(data=call_result)()

    return wrapper