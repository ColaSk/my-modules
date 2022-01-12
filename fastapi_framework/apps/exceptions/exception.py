from fastapi import Request
from apps.extensions import error_response
from fastapi.responses import JSONResponse


"""Exception definition
"""
class ExceptionBase(Exception):

    def __init__(self, status_code: int, msg: str):
        self.status_code = status_code
        self.msg = msg


class UnicornException(ExceptionBase):
    def __init__(self, status_code: int = 418, msg: str = "unicorn exception"):
        self.status_code = status_code
        self.msg = msg

"""Exception handling definition
# TODO: 1.迁移处理函数
# TODO: 2.适配HttpExc
# TODO: 3.状态码定义
"""
async def core_exception_handler(request: Request, exc: Exception):
    """Centralized exception handling"""

    # TODO: 异常记录

    responce = error_response(exc.status_code,  exc.msg)

    return JSONResponse(
        status_code=responce.code,
        content=responce.dict()
    )

