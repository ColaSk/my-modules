# -*- encoding: utf-8 -*-
'''
@File    :   setting.py
@Time    :   2022/01/20 17:39:34
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import os
from typing import Optional
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TODO：放在该放的位置
SECRET_KEY = "23bec386829bd6688b9940534113db03592ed7e5f70aa3a509a5a1d3f135a1e9"
ALGORITHM = "HS256"

class DBConfig(BaseModel):
    
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3306
    database: str
    user: str
    pwd: str


class LogConfig(BaseModel): ...


class TortoiseORMSetting(object):

    def __init__(self, db_config: DBConfig):

        self._db_config = db_config

    def _get_base_config(self, apps: dict) -> dict:

        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": self._db_config.host,
                        "port": self._db_config.port,
                        "database": self._db_config.database,
                        "user": self._db_config.user,
                        "password": self._db_config.pwd,
                        'charset': 'utf8mb4',
                    }
                }
            },
            "apps": apps,
            "use_tz": False,
            'timezone': 'Asia/Shanghai'
        } 
    
    @property
    def orm_link_config(self) -> dict:

        orm_apps_setting = {
             'models': {
                'models': [
                    'aerich.models',
                    'apps.models.models'
                ],
                'default_connection': 'default',
            }
        }

        return self._get_base_config(orm_apps_setting)


class Setting(BaseModel):

    db: DBConfig


# 临时配置 后续添加配置文件
db_config = {
    'host': '127.0.0.1',
    'port': 11000,
    'database': 'fastapitest',
    'user': 'root',
    'pwd': 'root'
}

setting = Setting(db=DBConfig(**db_config))

ORM_LINK_CONF = TortoiseORMSetting(setting.db).orm_link_config

