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
from asyncio.coroutines import iscoroutine
import threading
from hbmqtt.client import MQTTClient
from typing import Any, AsyncGenerator, Callable, Union

class AsyncMQTTClient(object):

    def __init__(
        self, 
        client_id: str = None, 
        config: dict = None, 
        loop = None,
        sem_num: int = 50):

        self._callback_mutex = threading.RLock()
        self._on_message_filtered = dict()
        
        self.sem = asyncio.Semaphore(sem_num, loop=loop)
        self.client = MQTTClient(client_id, config, loop)

    def on_message(self, client: MQTTClient, message) -> None: ...

    def on_publish(self, client: MQTTClient) -> None: ...

    def message_callback_add(self, topic: str, callback: Union[Callable, AsyncGenerator]):

        if callback is None or topic is None:
            raise ValueError("sub and callback must both be defined.")

        with self._callback_mutex:
            self._on_message_filtered[topic] = callback
  
    def message_callback_remove(self, topic: str):
        """Remove a message callback previously registered with
        message_callback_add()."""

        if topic is None:
            raise ValueError("topic must defined.")

        with self._callback_mutex:
            try:
                del self._on_message_filtered[topic]
            except KeyError:  # no such subscription
                pass

    async def message_hanlder(self, message):

        async def async_func(func, *args, **kwargs):
            return func(*args, **kwargs)

        packet = message.publish_packet
        topic = packet.variable_header.topic_name
        
        with self._callback_mutex:
            callback = self._on_message_filtered.get(topic, self.on_message)
        
        if not iscoroutine(callback):
            callback = async_func(callback, self.client, message)
        else:
            callback = callback(self.client, message)

        task = asyncio.create_task(callback)

    async def loop_forever(self):

        run = True
        while run:

            message = await self.client.deliver_message()

            async with self.sem:
                await self.message_hanlder(message)

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.client, __name)

    # def __del__(self):
    #     self.client.disconnect()

    

        