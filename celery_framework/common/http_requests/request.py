# -*- encoding: utf-8 -*-
'''
@File    :   request.py
@Time    :   2021/10/29 14:28:03
@Author  :   sk 
@Version :   1.0
@Contact :   kaixuan.sun@boonray.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import requests

class Request:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.http = f"http://{self.host}:{self.port}"
        self.headers = {
            "User-Agent": "PostmanRuntime/7.26.8"
        }
    
    def request(self, method, url, **kw):
        m = method.upper()
        if not url.startswith("http://"):
            url = f"{self.http}{url}"
        
        if not kw.get("headers"):
            kw["headers"] = self.headers

        if m == "GET":
            return requests.get(url, **kw)
        
        if m == "POST":
            return requests.post(url, **kw)

        return None

    def post(self, **kw):
        url = kw.pop("url")
        return self.request("post", url, **kw)

    def get(self, **kw):
        url = kw.pop("url")
        return self.request("get", url,**kw)

    def set_header(self, **kw):
        self.headers.update(kw)
    
    def is_ok(self, status_code):
        if status_code == requests.codes.ok:
            return True
        return False