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
from tortoise.transactions import atomic
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from apps.exceptions.exception import NotFound
from datetime import date, datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from config.setting import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/admin/login") # TODO：放在他应该在的地方

class UserOperator(object): 
    
    @staticmethod
    def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建token

        Args:
            data (dict): token data
            expires_delta (Optional[timedelta], optional): 两个时间的差值. Defaults to None.

        Returns:
            _type_: _description_
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() +  timedelta(minutes=15)  

        to_encode.update({'exp': expire})
        
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def check_token(token: str = Depends(oauth2_scheme)):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        except JWTError as e:
            raise e
    
    @classmethod
    def curr_user(cls, token: dict = Depends(oauth2_scheme)):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        except JWTError as e:
            raise e   

    @classmethod
    async def login(cls, username: str, password: str) -> Tuple[str, dict]:

        user = await User.get_or_none(name=username)

        if not user:
            raise NotFound(msg=f' not found username: {username} user')

        if not user.check_password(password):
            raise Exception('password error')

        token = cls.create_token({'sub': user.name})

        userdata = user.to_dict(('id', 'created_time', 'name'))
        
        return token, userdata
     
    @classmethod
    def logout(cls, username: str): ...

    @classmethod
    async def create(cls, username: str, password: str):
        user = User(name=username)
        user.password = password # 密码哈希
        await user.save()
        return user
        


