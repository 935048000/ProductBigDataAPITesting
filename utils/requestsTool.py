# -*- coding: utf-8 -*-
# @Time : 2020-3-12 16:24
# @Author : chenhao
# @FileName: requestsTool.py
# @Software: PyCharm
# @E-Mail: chenhao886640@gmail.com

import requests
import json
from utils.Log import logger
import ast

logger = logger
class requestsTool():
    def __init__(self):
        self.result = None
    
    # 定义一个方法，传入需要的参数url和data
    def send_post(self, url, data):
        """
        参数必须按照url、data顺序传入
        :param url:
        :param data:
        :return: 返回码，返回数据
        """

        # 因为这里要封装post方法，所以这里的url和data值不能写死
        self.result = requests.post(url=url, data=data)
        if(self.result.status_code == 404):
            return self.result.status_code, self.result.text
        else:
            return self.result.status_code, ast.literal_eval (self.result.text)
        

    def send_get(self, url, data):
        """
        GET
        :param url:
        :param data:
        :return:
        """
        self.result = requests.get(url=url, data=data)
        if (self.result.status_code == 404):
            return self.result.status_code, self.result.text
        else:
            return self.result.status_code, ast.literal_eval (self.result.text)


if __name__ == '__main__':  # 通过写死参数，来验证我们写的请求是否正确
    data = {'year': '2019'}
    errcode,result = requestsTool ().send_post ('http://49.235.241.182:8080/price/monCorrespondingPeriod', data)
    print (result)
    print (errcode)
    # result = requests.post (url="http://49.235.241.182:8080/price/monCorrespondingPeriod1", data=data)
    # print(result.status_code)
    # r = result.text
    # print(type(r))
    # print ( ast.literal_eval(r)['errcode'])