# -*- encoding: utf-8 -*-
'''
@File    :   mixin.py
@Time    :   2021/12/29 09:36:59
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from contextlib import ContextDecorator
from flask_sqlalchemy import BaseQuery
from .dbbase import db

# ! 缺少DB 不能被引用使用，使用需复制到自己项目中配合使用，后续想办法引入
# ! 采用自定义db方式引入db，可通过内部flask初始化进行使用

class ModelOperate(object):

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def list(cls, **kwargs) -> BaseQuery:
        return cls.query.filter_by(**kwargs)

    @staticmethod
    def rollback():
        db.session.rollback()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def flush():
        db.session.flush()

    def delete(self):
        """删除对象"""
        db.session.delete(self)
        self.commit()

    def delete_flush(self):
        db.session.delete(self)
        self.flush()

    @classmethod
    def add(cls, instance):
        """add and commit one instance"""

        db.session.add(instance)
        cls.commit()
        return instance

    @classmethod
    def add_flush(cls, instance):
        """add and flush one instance"""

        db.session.add(instance)
        cls.flush()

    def save(self):
        """add self and commit"""

        db.session.add(self)
        self.commit()
        return self

    def save_flush(self):
        """add self and flush"""

        db.session.add(self)
        self.flush()

        return self

    def update(self, **kwargs):
        """更新字段的值

        调用 .save() 保存
        """

        for key, value in kwargs.items():
            if value != getattr(self, key):
                setattr(self, key, value)
        instance = self.save()
        return instance

    def update_flush(self, **kwargs):
        """更新字段的值

        调用 .save_flush()
        """

        for key, value in kwargs.items():
            if value != getattr(self, key):
                setattr(self, key, value)
        instance = self.save_flush()
        return instance

    @classmethod
    def execute(cls, sql: str) -> bool:
        """执行 sql 语句

        execute and commit
        """

        result = db.session.execute(sql)
        db.session.commit()
        return result
    
    @classmethod
    def exists(cls, **kwargs):
        return cls.get(**kwargs) != None

    @classmethod
    def bulk_insert_mappings(cls, mappings, return_defaults=False, render_nulls=False):
        """批量插入"""

        db.session.bulk_insert_mappings(
            cls, mappings=mappings, return_defaults=return_defaults, render_nulls=render_nulls
        )

        cls.commit()
        return True

    @classmethod
    def bulk_insert_mappings_flush(cls, mappings, return_defaults=False, render_nulls=False):
        """批量插入"""

        db.session.bulk_insert_mappings(
            cls, mappings=mappings, return_defaults=return_defaults, render_nulls=render_nulls
        )

        cls.flush()
        return True

    @staticmethod
    def to_dict(instance, selects: tuple = None, excludes: tuple = None) -> dict:
        # 返回 dict 格式数据, 获取 instance 的各个字段以及属性

        if instance:
            if not hasattr(instance, '__table__'):
                raise Exception('<%r> does not have attribute for __table__' % instance)
            had_fields = instance.__table__.columns
            if selects:
                return {i: getattr(instance, i) for i in selects}
            elif excludes:
                return {i.name: getattr(instance, i.name) for i in had_fields if i.name not in excludes}
            else:
                return {i.name: getattr(instance, i.name) for i in had_fields}
        else:
            return {}

    @classmethod
    def to_representation(
            cls, instance, selects: tuple = None, excludes: tuple = None,
            second_attrs: tuple = None, children_attrs: tuple = None
    ) -> dict:

        info = cls.to_dict(instance, excludes, selects)

        if second_attrs:
            for attr in second_attrs:
                info.update({attr: cls.to_dict(getattr(instance, attr))})

        if children_attrs:
            for attr in children_attrs:
                children = getattr(instance, attr)
                for child in children:
                    info.setdefault(attr, []).append(cls.to_dict(child))

        return info


class Atomic(ContextDecorator):
    """
    Transaction context
    """

    def __init__(self, db, savepoint=None):
        self.db = db  # db
        self.savepoint = savepoint  # save point

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type is None:
            try:
                self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
        else:
            self.db.session.rollback()


def atomic(using=None, savepoint=None):
    # Bare decorator: @atomic -- although the first argument is called
    # `using`, it's actually the function being decorated.
    if callable(using):
        return Atomic(db, savepoint)(using)
    # Decorator: @atomic(...) or context manager: with atomic(...): ...
    else:
        if not using:
            using = db
        return Atomic(using, savepoint)


def atomic_begin_nested(using=None):
    # Nested transaction
    # simple encapsulation
    if not using:
        using = db
    
    return using.session.begin_nested()