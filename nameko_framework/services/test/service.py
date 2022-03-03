# -*- encoding: utf-8 -*-
'''
@File    :   service.py
@Time    :   2021/06/18 10:37:11
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import logging
from common.wrappers import rpc
from common import SeriviceBase

logger = logging.getLogger(__name__)

class TestService(SeriviceBase):

    name = "Test"

    @rpc
    def test(self, *args, **kwargs):
        logger.info("test success")
        return True
