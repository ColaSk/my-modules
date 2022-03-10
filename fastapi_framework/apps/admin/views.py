from typing import Any, Optional
from fastapi import APIRouter, Response, Depends
from apps.extensions import success_response
from apps.extensions import RequestBase, RequestDependBase
from apps.exceptions.exception import UnicornException
from apps.extensions.route import MyRoute

router = APIRouter(route_class=MyRoute)

class LoginRequest(RequestBase):
    username: str
    password: str

@router.post('/login', status_code=201)
async def Login(
    body: LoginRequest,
    response: Response,
    header_and_cookie: dict = Depends(RequestDependBase)):

    response.set_cookie(key="csrftoken", value="fake-cookie-session-value") # 设置token
    return success_response(data=header_and_cookie)