# -*-coding:utf-8-*-
"""
Created on 2024/11/16

@author: 臧韬

@desc: 默认描述
"""

from wanyun_JitSdk import JitApi
from wanyun_JitSdk import JitApiRequest

authApi = JitApi("http://zangtao.cpolar.top/api/whwy/ZTTest21")  # 授权方的api访问地址
authApi.setAccessKey("testtest")  # api授权元素配置的accessKey
authApi.setAccessSecret("32fca7ea52834355be0f978c9bf067eed05606")  # api授权元素配置的accessSecret
authApi.setApi("services.svc1.func3")  # 需要调用的api
req = JitApiRequest()
req.setMethod("POST")  # 接口请求方式，默认为POST
req.setParams({"data": {
    "a": "ttt",
    "b": "ttt"
}})  # 接口参数
resp = req.execute(authApi)
print(resp.data)
