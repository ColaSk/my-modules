# -*- encoding: utf-8 -*-
'''
@File    :   mqtt_client.py
@Time    :   2022/02/22 18:02:58
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import asyncio

from hbmqtt.client import MQTTClient
from typing import Any

class AsyncMQTTClient(object):

    def __init__(self, client_id=None, config=None, loop=None):
        self.client = MQTTClient(client_id, config, loop)

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.client, __name)

    

        