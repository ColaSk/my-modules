from pydantic import BaseModel, Field
from fastapi import Cookie
from utils import get_curr_time

class RequestBase(BaseModel):
    reqtime: str = Field(get_curr_time(), description='request time') # TODO: 动态时间

def request_base(request_cls: RequestBase = None, cookie: Cookie = None, **kewags):

    request = dict(
        cookie = Cookie(None),
        request = RequestBase
    )

    if request_cls:
        request['request'] = request_cls

    if cookie:
        request['request'] = cookie

    request.update(kewags)
    
    return request