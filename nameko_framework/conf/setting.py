# -*- encoding: utf-8 -*-
'''
@File    :   myconf.py
@Time    :   2021/06/18 15:34:09
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import os
from . import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project base dir
 
class Setting:
    """Some parameter settings for all services in the whole project
    """
    
    # Registration services
    INSTALLED_SERVICES = ["services:TestService"]
    
    CONFIG_YAML = getattr(config, 'CONFIG_YAML', "./conf/config.yaml")

    LOG_DIR = f'{BASE_DIR}/logs'
