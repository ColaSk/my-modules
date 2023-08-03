# -*- encoding: utf-8 -*-
'''
@File    :   edict.py
@Time    :   2023/08/03 09:42:46
@Author  :   KaiXuan Sun (Sk)
@Version :   1.0
@Contact :   sunkaixuan@zhidemai.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib


import typing as t
from typing import Any


class Argument(object):
    """映射参数
        ex:
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        class WebSiteConfig(DictBase):
            id = StrArgument('ID')

    """

    def __init__(self,
                 name: str,
                 type: t.Optional[t.Callable] = None,
                 required: bool = False,
                 default: Any = None,
                 model: t.Optional["DictBase"] = None) -> None:
        """
        name: str 字典对应的key
        type: Any 需要转化的类型
        required: bool = False 是否必须
        default: Any = None 默认值
        model: t.Optional["DictBase"] = None 所在类的模型实例
        """
        self.name = name
        self.type = type
        self.required = required
        self.default = default
        self.model = model
        # self.validate = validate

    def type_converter(self, value: Any) -> Any:
        """类型转化器
        将参数转化为设置的类型
        # TODO: 多种类型之间转化, 需要重新构建
        """
        if not self.type or isinstance(value, self.type):
            return value
        val = self.type(value)
        return val

    @property
    def value(self):
        """获取数据"""
        if self.required and self.name not in self.model:
            raise KeyError(f'当前参数<{self.name}>不存在')

        val = self.model.get(self.name, self.default)
        if val:
            return self.type_converter(val)
        return self.default

    @property
    def source(self):
        """获取源数据"""
        return self.model.get(self.name)

    def set_model(self, _model: 'DictBase'):
        self.model = _model

    def __getattr__(self, __name: str) -> Any:
        obj = self.value
        if not hasattr(obj, __name):
            raise AttributeError(
                f"{obj.__class__} 不存在属性: {__name}")
        attr = getattr(obj, __name)
        return attr


class StrArgument(Argument):
    def __init__(self,
                 name: str,
                 default: str = '',
                 model: t.Optional["DictBase"] = None) -> None:
        super().__init__(name, str, default, model)


class DictBase(dict):

    def __getattribute__(self, __name: str) -> Any:
        attribute = super().__getattribute__(__name)
        if isinstance(attribute, Argument) and not getattr(attribute, 'model'):
            attribute.set_model(self)
        return attribute

    def __call__(self, value: dict) -> 'DictBase':
        if isinstance(value, dict):
            self.update(value)
            return self
        raise TypeError('无法进行类型转化')
