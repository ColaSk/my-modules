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
import sys
from .command import (RenameCommand, CopyCommand, DeleteCommand, 
                      DirRenameCommand, DirCopyCommand, DirDeleteCommand)
from .interfaces import AcidContext, CommandOperator
from .command_container import CommandQueue, CommandStack

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

class Acid(CommandOperator):

    COMMAND_SET = {}

    def __init__(self):
        self._cque = CommandQueue()
        self._cstack = CommandStack()
    
    def rename(self, src_path: str, dest_path: str, exec: bool = False):
        cmd_cls = self.COMMAND_SET.get(sys._getframe().f_code.co_name)
        cmd = cmd_cls(src_path, dest_path)
        if exec:
            cmd.execute()
            self._cstack.put(cmd)
        else:
            self._cque.put(cmd)

    def copy(self, src_path: str, dest_path: str, exec: bool = False):
        cmd_cls = self.COMMAND_SET.get(sys._getframe().f_code.co_name)
        cmd = cmd_cls(src_path, dest_path)
        if exec:
            cmd.execute()
            self._cstack.put(cmd)
        else:
            self._cque.put(cmd)

    def delete(self, path: str, exec: bool = False):
        cmd_cls = self.COMMAND_SET.get(sys._getframe().f_code.co_name)
        cmd = cmd_cls(path)
        if exec:
            cmd.execute()
            self._cstack.put(cmd)
        else:
            self._cque.put(cmd)
    
    def commit(self):
        while not self._cque.empty:
            cmd = self._cque.get()
            cmd.execute()
            self._cstack.put(cmd)

    def rollback(self):
        while not self._cstack.empty:
            cmd = self._cstack.get()
            cmd.undo()


class AcidFile(Acid, AcidContext):
 
    COMMAND_SET = {
        'rename': RenameCommand,
        'copy': CopyCommand,
        'delete': DeleteCommand
    }


class AcidDir(Acid, AcidContext):

    COMMAND_SET = {
        'rename': DirRenameCommand,
        'copy': DirCopyCommand,
        'delete': DirDeleteCommand
    }
