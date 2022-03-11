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


class User(object):

    def __init__(self, username: str):
        self._username = username
    
    @property
    def username(self):
        return self._username

    def check_password(self, password: str) -> bool:
        # 检验密码
        ...

class UserOperator(object): 

    def login(self, username: str, password: str):

        user = User(username)

        if user.check_password(password):
            pass
        else:
            pass
    

    def logout(self, username: str): ...