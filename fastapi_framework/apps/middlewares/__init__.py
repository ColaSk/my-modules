# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2022/01/20 17:41:07
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from .middleware import before_request

app_middleware = [before_request]