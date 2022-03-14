# -*- encoding: utf-8 -*-
'''
@File    :   tokens.py
@Time    :   2022/03/14 14:27:37
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.setting import SECRET_KEY, ALGORITHM


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建token

    Args:
        data (dict): token data 可以包含用户信息: name create_time id
        expires_delta (Optional[timedelta], optional): 两个时间的差值. Defaults to None.

    Returns:
        str: token string
    """
    now = datetime.now()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now +  timedelta(minutes=30)

    token_dict = {
        'exp': expire,
        'iat': now,
        'data': data.copy()
    }


    return jwt.encode(token_dict, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """验证token

    Args:
        token (str): tokens tring

    Raises:
        e: _description_

    Returns:
        dict: token info
    """    
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
    except JWTError as e:
        raise e
