from pydantic import BaseModel
from fastapi import Depends


from .depends import CookieDependBase, HeaderDependBase


class RequestBase(BaseModel): ...


def request_base(
    header: HeaderDependBase = Depends(HeaderDependBase), 
    cookie: dict = Depends(CookieDependBase)
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
        cookie: CookieDependBase = Depends(CookieDependBase)
    ):
        self.header = header
        self.cookie = cookie