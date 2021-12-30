# -*- encoding: utf-8 -*-
'''
@File    :   service.py
@Time    :   2021/06/18 10:37:11
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from nameko.rpc import rpc

class TestService:

    name = "Test"

    @rpc
    def test(self, *args, **kwargs):
        print("test success")
        return True
