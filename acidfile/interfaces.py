# -*- encoding: utf-8 -*-
'''
@File    :   Interfaces.py
@Time    :   2021/12/29 17:40:25
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

from abc import ABCMeta, abstractmethod
from .command_container import CommandQueue, CommandStack


class Acid(metaclass=ABCMeta):

    def __init__(self):
        self._cque = CommandQueue()
        self._cstack = CommandStack()
    
    @abstractmethod
    def commit(self): pass
    
    @abstractmethod
    def rollback(self): pass


class AcidContext:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:
            try:
                self.commit()
            except Exception as e:
                self.rollback()
                raise e
        else:
            self.rollback()


class CommandOperator(metaclass=ABCMeta):

    @abstractmethod
    def rename(self, src_path: str, dest_path: str, exec: bool = False): pass

    @abstractmethod
    def copy(self, src_path: str, dest_path: str, exec: bool = False): pass

    @abstractmethod
    def delete(self, path: str, exec: bool = False): pass