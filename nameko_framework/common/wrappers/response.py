# -*- encoding: utf-8 -*-
'''
@File    :   response.py
@Time    :   2021/07/08 18:44:01
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
# response define

class ResponseBase:

    def __init__(self, data=None, status_code=0, msg='', code=0) -> None:
        self.status_code = status_code
        self.msg = msg
        self.code = code
        self.data = data
    
    def __call__(self):
        return vars(self)
    
class RpcSuccessResponse(ResponseBase):
    """RPC 调用返回响应"""

    def __init__(self, data, status_code=200, msg="success", code=10200) -> None:
        super().__init__(status_code=status_code, msg=msg, code=code, data=data)

class RpcErrorResponse(ResponseBase):
     def __init__(self, data=None, status_code=400, msg="error", code=10400) -> None:
        super().__init__(status_code=status_code, msg=msg, code=code, data=data)

if __name__ == "__main__":
    print(RpcErrorResponse("a")())