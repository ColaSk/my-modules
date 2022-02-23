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
from email import message
import threading
from hbmqtt.client import MQTTClient
from typing import Any, AsyncGenerator, Callable, Union

class AsyncMQTTClient(object):

    def __init__(
        self, 
        client_id: str = None, 
        config: dict = None, 
        loop = None):

        self._callback_mutex = threading.RLock()
        self._on_message_filtered = dict()

        self.client = MQTTClient(client_id, config, loop)

        # self.

    def on_message(self, client: MQTTClient, message) -> None: ...

    def on_publish(self, client: MQTTClient) -> None: ...

    def message_callback_add(self, topic: str, callback: Union[Callable, AsyncGenerator]):

        if callback is None or topic is None:
            raise ValueError("sub and callback must both be defined.")

        with self._callback_mutex:
            self._on_message_filtered[topic] = callback

    
    def message_callback_remove(self, sub):
        """Remove a message callback previously registered with
        message_callback_add()."""

        if sub is None:
            raise ValueError("sub must defined.")

        with self._callback_mutex:
            try:
                del self._on_message_filtered[sub]
            except KeyError:  # no such subscription
                pass

    async def message_hanlder(self, message):

        packet = message.publish_packet
        print("%s => %s" % (packet.variable_header.topic_name, str(packet.payload.data)))

    
    async def loop_forever(self):
        run = True
        while run:
            message = await self.client.deliver_message()
            await self.message_hanlder(message)

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.client, __name)

    

        