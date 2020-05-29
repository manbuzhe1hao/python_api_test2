from common import concant
from common.do_excel import DoExcel
import unittest
from common.request import Requests
from ddt import ddt,data
from common.logger import getloging
from common.mysql import MySqlMetul
from decimal import Decimal
logger=getloging('recharge')
do_excel= DoExcel(concant.excel_dir, 'recharge').get_data() #读取excel的值
request=Requests() #实例化requests请求
@ddt
class TestRecharge(unittest.TestCase): #继承unittest.TestCase
    def setUp(self):
        self.mysql=MySqlMetul()
        sql="SELECT LeaveAmount from future.member WHERE MobilePhone='15900002100'"
        self.pre_leaveamount=self.mysql.fetch_one(sql)[0]  #获取测试用例执行之前的数据库余额
    def login(self): #登录->用于获取cookies
        import requests
        data={'mobilephone':'15900002100','pwd':'123456'}
        resp=requests.get('http://test.lemonban.com/futureloan/mvc/api/member/login',params=data)
        return resp.cookies
    @data(*do_excel) #引入ddt
    def test_recharge(self,case):
       logger.info('开始执行{}条用例'.format(case['case_id']))
       cookies=TestRecharge().login()  #获取到cookies值
       resp=request.requests(case['method'],case['url'],case['data'],cookies=cookies)  #调用requests并发送请求
       try:
           logger.info('第{}条测试案例，PASS'.format(case['case_id']))
           if resp.json()['msg']=='充值成功':  #判断是否是充值成功，
               logger.info('数据库校验分支')
               sql = "SELECT LeaveAmount from future.member WHERE MobilePhone='15900002100'"
               leaveamount_after = str(MySqlMetul().fetch_one(sql)[0]) #获取充值成功之后数据库的余额
               import json
               case['data']=json.loads(case['data']) #将测试用例的参数变更为字典类型
               pre_leaveamount=Decimal(self.pre_leaveamount).quantize(Decimal("0.00")) #将测试用例执行之前的数据库余额保留两位小数
               case['data']['amount']=Decimal(case['data']['amount']).quantize(Decimal("0.00")) #将测试用例充值的金额保留两位小数
               resx =pre_leaveamount + case['data']['amount'] #测试用例执行之前的数据库余额加上测试用例充值的金额
               leaveamount_after=Decimal(leaveamount_after).quantize(Decimal("0.00")) #测试用例执行之后的数据库余额保留两位小数
               self.assertEqual(resx, leaveamount_after) #断言
           else:
               logger.info('数据库未校验分支')
           self.assertEqual(case['expected'],resp.json()['code']) #断言
           DoExcel(concant.excel_dir, 'recharge').write_data(case['case_id']+1,7,resp.json()['code']) #将响应返回的值回写表格中
           DoExcel(concant.excel_dir, 'recharge').write_data(case['case_id']+1, 8,'Pass')
       except AssertionError as e:
           logger.info('第{}条测试案例，False'.format(case['case_id']))
           logger.info('断言报错了{}'.format(e))
           DoExcel(concant.excel_dir, 'recharge').write_data(case['case_id']+1,7,resp.json()['code'])
           DoExcel(concant.excel_dir, 'recharge').write_data(case['case_id']+1, 8,'False')
           raise e  #抛出异常


if __name__ == '__main__':
    unittest.main()



