from typing import Optional
from fastapi import Cookie, Header, Depends


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


class CookieDependBase(object):

    def __init__(self, cookie: Optional[str] = Cookie(None)):
        self.cookie = cookie


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


def app_depend(header: HeaderDependBase = Depends(HeaderDependBase)):
    print(header.__dict__)

dependencies = [Depends(app_depend)]