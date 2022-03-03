# -*- encoding: utf-8 -*-
'''
@File    :   myconf.py
@Time    :   2021/10/26 18:03:07
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

import os
from kombu import Queue, Exchange

from .config import Config as GlobalConf


# 根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class RabbitMqConfig:

    HOST = GlobalConf.RABBITMQ_HOST
    PORT = GlobalConf.RABBITMQ_PORT
    USER = GlobalConf.RABBITMQ_USER
    PWD = GlobalConf.RABBITMQ_PASSWORD

    @classmethod
    def url(cls):
        return f'pyamqp://{cls.USER}:{cls.PWD}@{cls.HOST}:{cls.PORT}'


class RedisConfig:

    HOST = GlobalConf.REDIS_HOST
    PORT = GlobalConf.REDIS_PORT
    USER = GlobalConf.REDIS_USER
    PWD = GlobalConf.REDIS_PASSWD
    DB = getattr(GlobalConf, 'CELERY_REDIS_DB', 1)

    @classmethod
    def url(cls, db=None):
        if db:
            return f'redis://{cls.USER}:{cls.PWD}@{cls.HOST}:{cls.PORT}/{db}'
        else:
            return f'redis://{cls.USER}:{cls.PWD}@{cls.HOST}:{cls.PORT}/{cls.DB}'

class APIConfig:
    HOST = GlobalConf.API_SERVER_HOST
    PORT = GlobalConf.API_SERVER_PORT

    @classmethod
    def url(cls):
        return f'http://{cls.HOST}:{cls.PORT}'

class Setting:

    RABBITMQ_URL = RabbitMqConfig.url()
    REDIS_URL = RedisConfig.url()
    API_URL = APIConfig.url()

class LogConfig:

    LOG_DIR = os.path.join(BASE_DIR, "logs")
    os.makedirs(LOG_DIR, exist_ok=True)

class BeatConfig:
    BEAT_DIR = os.path.join(BASE_DIR, "celerybeat")
    os.makedirs(BEAT_DIR, exist_ok=True)

class CeleryConfig:

    broker_url = Setting.RABBITMQ_URL
    result_backend  = Setting.REDIS_URL
    
    """
    # ! 自定义队列后默认队列将不会生效, 需要自己手动添加
    """
    task_default_exchange = 'default-celery'
    task_default_queue = 'default-celery'
    task_default_exchange_type = 'direct'
    
    # 自定义配置 不属于celery内部配置选项
    define_exchange = {
        'default': Exchange(task_default_exchange, type=task_default_exchange_type),
        'test': Exchange('celery-test', type='direct')
    }
    
    # 定于队列
    task_queues = (
        Queue(task_default_queue, routing_key=task_default_queue, exchange=define_exchange.get('default')),
        Queue('celery-test-tasks', routing_key='test-tasks', exchange=define_exchange.get('test')),
    )
    task_routes = {
        'add': {
            'exchange': define_exchange.get('test').name,
            'routing_key': 'test-tasks'
        },
        'test_beat': {
            'exchange': task_default_exchange,
            'routing_key': task_default_queue
        }
    }

    # 周期任务定义
    beat_schedule = {
        ## 测试任务
        'test-every-10-seconds': {
            'task': 'test_beat',
            'schedule': 10
        }
    }

    # 本地时区
    enable_utc = False

    accept_content = ['json']
