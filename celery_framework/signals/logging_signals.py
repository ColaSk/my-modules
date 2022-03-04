# -*- encoding: utf-8 -*-
'''
@File    :   logging_signals.py
@Time    :   2021/11/01 10:57:46
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import logging
# ? 必须引入，否则 'AttributeError: module 'logging' has no attribute 'config''
import logging.config

from conf.logconf import LOGCONFIG as logconfig

from celery.signals import setup_logging

@setup_logging.connect
def setup_logging_handler(*args, **kwargs):
    logging.config.dictConfig(logconfig)

                          