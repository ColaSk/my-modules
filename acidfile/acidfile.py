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
from .command import (RenameCommand, CopyCommand, DeleteCommand)
from .interfaces import Acid, AcidContext, CommandOperator

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

class AcidFile(Acid, CommandOperator, AcidContext):

    def __init__(self):
        super().__init__()

    def rename(self, src_path: str, dest_path: str, exec: bool = False):
        cmd = RenameCommand(src_path, dest_path)
        if exec:
            cmd.execute()
            self._cstack.put(cmd)
        else:
            self._cque.put(cmd)

    def copy(self, src_path: str, dest_path: str, exec: bool = False):
        cmd = CopyCommand(src_path, dest_path)
        if exec:
            cmd.execute()
            self._cstack.put(cmd)
        else:
            self._cque.put(cmd)

    def delete(self, path: str, exec: bool = False):
        cmd = DeleteCommand(path)
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


class AcidDir(AcidContext):
    pass