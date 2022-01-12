from typing import Dict, Optional
from pydantic import BaseModel, Field
from fastapi import Cookie, Header, Depends
from utils import get_curr_time

class RequestBase(BaseModel): ...
    # reqtime: str = Field(get_curr_time(), description='request time') # TODO: 动态时间


def _cookie_depend(cookie: Optional[str] = Cookie(None)):
    return dict(cookie = cookie)
        
def _header_depend(
    content_type: Optional[str] = Header(None),
    content_length: Optional[str] = Header(None),
    host: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    accept: Optional[str] = Header(None),
    accept_encoding: Optional[str] = Header(None),
    connection: Optional[str] = Header(None)
):
    return {
        "Content-Type": content_type,
        "Content-Length": content_length,
        "Host": host,
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept-Encoding": accept_encoding,
        "Connection": connection
    }


class HeaderDependBase(object):

    def __init__(
        self,
        content_type: Optional[str] = Header(None),
        content_length: Optional[str] = Header(None),
        host: Optional[str] = Header(None),
        user_agent: Optional[str] = Header(None),
        accept: Optional[str] = Header(None),
        accept_encoding: Optional[str] = Header(None),
        connection: Optional[str] = Header(None)
    ):

        self.content_type = content_type
        self.content_length = content_length
        self.host = host
        self.user_agent = user_agent
        self.accept = accept
        self.accept_encoding = accept_encoding
        self.connection = connection


def request_base(
    header: HeaderDependBase = Depends(HeaderDependBase), 
    cookie: dict = Depends(_cookie_depend)
):

    request = dict(
        header = header,
        cookie = cookie
    )

    return request

class RequestDependBase(object):

    def __init__(
        self, 
        header: HeaderDependBase = Depends(HeaderDependBase), 
        cookie: dict = Depends(_cookie_depend)
    ):
        self.header = header
        self.cookie = cookie