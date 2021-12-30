from abc import ABCMeta
from .extensions import WorkerLogger

"""
服务基类,统一处理在基类中实现
"""
class SeriviceBase(metaclass=ABCMeta):
    
    logger = WorkerLogger()
