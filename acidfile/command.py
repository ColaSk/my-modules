# -*- encoding: utf-8 -*-
'''
@File    :   command.py
@Time    :   2021/12/28 10:53:54
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import os
import logging
import shutil
import tempfile

from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)

# 指令抽象类
class Command(object, metaclass=ABCMeta):

    def __init__(self):
        self.exec = False
    
    def execute(self):
        self.exec = True
    
    def undo(self):
        if not self.exec:
            raise Exception("command not executed, so it cannot be recovered")
        self.exec = False

# 重命名指令
class RenameCommand(Command):

    def __init__(self, src_path: str, dest_path: str):
        self.src_path, self.dest_path = src_path, dest_path
        super().__init__()

    def execute(self):
        os.rename(self.src_path, self.dest_path)
        super().execute()
    
    def undo(self):
        super().undo()
        os.rename(self.dest_path, self.src_path)

# 复制
class CopyCommand(Command):

    def __init__(self, src_path: str, dest_path: str):
        super().__init__()
        self.src_path, self.dest_path = src_path, dest_path
        
    def execute(self):
        super().execute()
        shutil.copy(self.src_path, self.dest_path)
    
    def undo(self):
        super().undo()
        os.remove(self.dest_path)

# 删除
class DeleteCommand(Command):

    def __init__(self, src_path: str):
        super().__init__()
        self.src_path = src_path
        self.tempdir = tempfile.TemporaryDirectory()

        filename = self.src_path.split('/')[-1]
        self.tempfile_path = os.path.join(self.tempdir.name, filename)

    def execute(self):
        super().execute()
        shutil.copy(self.src_path, self.tempfile_path)
        os.remove(self.src_path)
    
    def undo(self):
        super().undo()
        shutil.copy(self.tempfile_path, self.src_path)
    
    def __del__(self):
        self.tempdir.cleanup()


class DirRenameCommand(RenameCommand):
    pass


class DirCopyCommand(Command):

    def __init__(self, src_path: str, dest_path: str, ignored: list = None):
        super().__init__()
        self.src_path = src_path
        self.dest_path = dest_path
        self.ignored = ignored


    def execute(self):
        super().execute()
        shutil.copytree(
            self.src_path, 
            self.dest_path,
            ignore=shutil.ignore_patterns(*self.ignored), 
            dirs_exist_ok=True)
    
    def undo(self):
        super().undo()
        shutil.rmtree(self.dest_path)


class DirDeleteCommand(Command):

    def __init__(self, src_path: str):
        super().__init__()
        self.src_path = src_path
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdir_path = self.tempdir.name

    def execute(self):
        super().execute()
        shutil.copytree(
            self.src_path, 
            self.tempdir_path,
            dirs_exist_ok=True
        )
        shutil.rmtree(self.src_path)
    
    def undo(self):
        super().undo()
        shutil.copy(self.tempdir_path, self.src_path)
    
    def __del__(self):
        self.tempdir.cleanup()