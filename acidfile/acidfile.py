# -*- encoding: utf-8 -*-
'''
@File    :   acidfile.py
@Time    :   2021/12/28 09:52:50
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import logging
from .command_container import CommandQueue, CommandStack
from .command import (Command, RenameCommand, CopyCommand, DeleteCommand)

"""文件操作的事务
# 文件操作:
    - 复制
    - 剪切(移动)
    - 删除
    - 重命名
# 文件夹操作
    - 复制
    - 剪切(移动)
    - 删除
    - 重命名
"""

logger = logging.getLogger(__name__)

class AcidFile(object):

    def __init__(self):
        self._cque = CommandQueue()
        self._cstack = CommandStack()

    def rename(self, src_path: str, dest_path: str) -> Command:
        cmd = RenameCommand(src_path, dest_path)
        self._cque.put(cmd)
        return cmd

    def copy(self, src_path: str, dest_path: str) -> Command:
        cmd = CopyCommand(src_path, dest_path)
        self._cque.put(cmd)
        return cmd

    def delete(self, path: str) -> Command:
        cmd = DeleteCommand(path)
        self._cque.put(cmd)
        return cmd

    def commit(self):
        while not self._cque.empty:
            cmd = self._cque.get()
            cmd.execute()
            self._cstack.put(cmd)

    def rollback(self):
        while not self._cstack.empty:
            cmd = self._cstack.get()
            cmd.undo()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:
            try:
                self.commit()
            except Exception as e:
                logger.error(e.__str__())
                self.rollback()
        else:
            logger.error(f'exc_type: {exc_type}, exc_value: {exc_val}')
            self.rollback()