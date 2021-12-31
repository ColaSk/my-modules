# -*- encoding: utf-8 -*-
'''
@File    :   rpc_service_define.py
@Time    :   2021/12/31 10:54:42
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
"""外部应用定义nameko rpc service 的基类

example:

    Testservice(NamekoRpcServiceBase):
        service_name = "Test"
        service_methods = "test"
    
    with ClusterRpcProxy(config) as cluster_rpc:
        test_service = Testservice(cluster_rpc)
        test_service.call()
        test_service.call_async()

"""

class NamekoRpcServiceBase:

    service_name = None
    service_methods = None

    def __init__(self, rpc) -> None:
        self.rpc = rpc

    def call(self, *args, **kwargs):
        """同步调用"""
        return getattr(
            getattr(self.rpc, self.service_name), 
            self.service_methods
        )(*args, **kwargs)

    def call_async(self, *args, **kwargs):
        """异步调用"""
        return getattr(
            getattr(self.rpc, self.service_name), 
            self.service_methods
        ).call_async(*args, **kwargs)