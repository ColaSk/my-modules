from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from apps.extensions import success_response
from apps.extensions import RequestDependBase
from apps.extensions.route import MyRoute

from .services import UserOperator, CurrUser
from .schemas import CreateUserRequest


router = APIRouter(route_class=MyRoute)

@router.post('/login', status_code=201)
async def Login(
    bady: OAuth2PasswordRequestForm = Depends(),
    header_and_cookie: dict = Depends(RequestDependBase)):
    """登录"""

    token, userdata = await UserOperator.login(bady.username, bady.password)
    result = {'token': token, 'user': userdata}
    return success_response(data=result)


@router.post('/users', status_code=201)
async def create_user(
    body: CreateUserRequest,
    header_and_cookie: dict = Depends(RequestDependBase)):
 
    user = await UserOperator.create(**(body.dict()))
    return success_response(data=user)


@router.get('/user', status_code=201)
async def get_curr_user(
    curr_user: CurrUser = Depends(UserOperator.curr_user)):

    return success_response(await curr_user.to_dict_async())