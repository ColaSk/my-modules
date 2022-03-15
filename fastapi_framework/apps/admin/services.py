# -*- encoding: utf-8 -*-
'''
@File    :   services.py
@Time    :   2022/03/10 17:18:26
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from apps.models.models import User 
from apps.models.mixin import ModelObject
from apps.extensions import create_token, verify_token
from tortoise.transactions import atomic
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from apps.exceptions.exception import NotFound
from typing import Tuple


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/admin/login") # TODO：放在他应该在的地方


class UserObject(object):

    def __init__(self, id: int) -> None:
        self._user = ModelObject(User, id).object(is_del=False)

    @property
    async def user(self):
        return await self._user


class CurrUser(UserObject): 
    """当前用户
    单独处理权限问题
    """

    async def to_dict_async(self):
        data_attr = ('id', 'created_time', 'name')
        user = await self.user
        return user.to_dict(data_attr)


class UserOperator(object): 
      
    @classmethod
    def curr_user(cls, token: dict = Depends(oauth2_scheme)) -> CurrUser:
        """获取当前用户"""
        userdata = verify_token(token)
        return CurrUser(userdata.get('data', {}).get('id'))

    @classmethod
    async def login(cls, username: str, password: str) -> Tuple[str, dict]:

        user = await User.get_or_none(name=username, is_del=False)

        if not user:
            raise NotFound(msg=f' not found username: {username} user')

        if not user.check_password(password):
            raise Exception('password error')

        userdata = user.to_dict(('id', 'created_time', 'name'))

        token = create_token(userdata)

        return token, userdata
     
    @classmethod
    def logout(cls, username: str): ...

    @classmethod
    async def create(cls, username: str, password: str):
        user = User(name=username)
        user.password = password # 密码哈希
        await user.save()
        return user
        


