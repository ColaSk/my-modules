
from pydantic import BaseModel
from typing import Any

class ResponseBase(BaseModel):
    success: bool
    data: Any
    code: int
    msg: str = None

def success_response(data: Any, 
                     code: int = 201, 
                     msg : str = None, 
                     res_cls: ResponseBase = ResponseBase):

    return res_cls(success=True, data=data, code=code, msg=msg)


def error_response(code: int = 401, 
                   msg : str = 'unknown error', 
                   res_cls: ResponseBase = ResponseBase):

    return res_cls(success=False, data=None, code=code, msg=msg)