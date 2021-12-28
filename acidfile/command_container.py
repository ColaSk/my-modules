# -*- encoding: utf-8 -*-
'''
@File    :   command_container.py
@Time    :   2021/12/28 13:38:06
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from queue import Queue, LifoQueue

class CommandQueue(object):
    
    def __init__(self, maxsize=0):
        self._queue = Queue(maxsize)
    
    @property
    def size(self) -> int:
        return self._queue.qsize()

    @property
    def empty(self) -> bool:
        return self._queue.empty()

    def get(self, block=True, timeout=None):
        return self._queue.get(block, timeout)
    
    def put(self, item, block=True, timeout=None):
        return self._queue.put(item, block, timeout)
    

class CommandStack(CommandQueue):

    def __init__(self, maxsize=0):
        self._queue = LifoQueue(maxsize)
    



