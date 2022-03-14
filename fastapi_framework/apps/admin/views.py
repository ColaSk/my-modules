from typing import Any, Optional
from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from apps.extensions import success_response
from apps.extensions import RequestBase, RequestDependBase
from apps.exceptions.exception import UnicornException
from apps.extensions.route import MyRoute

from .services import UserOperator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/admin/login") # TODO：放在他应该在的地方
router = APIRouter(route_class=MyRoute)

class LoginRequest(RequestBase):
    username: str
    password: str

@router.post('/login', status_code=201)
async def Login(
    bady: OAuth2PasswordRequestForm = Depends(),
    header_and_cookie: dict = Depends(RequestDependBase)):
    """登录"""

    token, userdata = await UserOperator.login(bady.username, bady.password)
    result = {'token': token, 'user': userdata}
    return success_response(data=result)

class CreateUserRequest(RequestBase):
    username: str
    password: str

@router.post('/users', status_code=201)
async def create_user(
    body: CreateUserRequest,
    header_and_cookie: dict = Depends(RequestDependBase)):
 
    user = await UserOperator.create(**(body.dict()))

    return success_response(data=user)


@router.get('/user', status_code=201)
async def list_users(curr_user: str = Depends(UserOperator.curr_user)):
    return success_response({"curr_user": curr_user})