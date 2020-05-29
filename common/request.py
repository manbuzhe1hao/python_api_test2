import requests
from common.config import ReadConfig

class Requests:
    def requests(self,method,url,data,cookies=None):
        pre_url=ReadConfig().get('api','pre_url') #读取配置文件中的地址
        url=pre_url+url #拼接地址
        if data is not None and type(data)==str: #requests请求中，只支持字典方式传值
            import json
            data=json.loads(data) #所以需要将data的类型转换成字典传入
        if method=='get' or  method=='GET':
            return requests.request(method=method,url=url,params=data,cookies=cookies)
        elif method=='post' or method =='POST':
            return requests.request(method=method, url=url, data=data, cookies=cookies)
        else:
            return  print('请填写正确的请求方式！！')




