# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2023/08/03 09:44:39
@Author  :   KaiXuan Sun (Sk)
@Version :   1.0
@Contact :   sunkaixuan@zhidemai.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from enhance_dict.edict import DictBase, Argument
from enhance_dict.edict import StrArgument


class Param(DictBase):
    id = StrArgument('ID')


class WebSiteConfig(DictBase):

    id = StrArgument('ID')
    param = Argument('Params', Param)


class PlanConfig(DictBase):
    ...


class TaskConfig(DictBase):
    ...


if __name__ == '__main__':
    # from marshmallow import Schema,fields,ValidationError
    website_config = WebSiteConfig()
    website_config.update({'ID': 1, 'Params': {'ID': 2}})
    print(website_config.id.value)
    print(website_config["Params"]["ID"])
