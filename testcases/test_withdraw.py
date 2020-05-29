from common import concant
from common.do_excel import DoExcel
from common.logger import getloging
import unittest
from common.request import Requests
from ddt import ddt,data
from common.mysql import MySqlMetul
from decimal import Decimal

do_excel= DoExcel(concant.excel_dir, 'withdraw').get_data() #读取excel的值
request=Requests() #实例化requests请求
logger=getloging('withdraw')
@ddt
class TestWithdraw(unittest.TestCase): #继承unittest.TestCase
    def setUp(self):
        sql = "SELECT LeaveAmount from future.member WHERE MobilePhone='15900002100'"
        self.pre_results = MySqlMetul(return_dict=True).fetch_all(sql)[0]['LeaveAmount'] # 从数据库获取提现之前的余额
        logger.info('提现之前的余额',self.pre_results)

    def login(self):
        import requests
        data={'mobilephone':'15900002100','pwd':'123456'}
        resp=requests.get('http://test.lemonban.com/futureloan/mvc/api/member/login',params=data)
        return resp.cookies
    @data(*do_excel) #引入ddt
    def test_withdraw(self,case):
       logger.info('开始执行{}条测试案例'.format(case['case_id']))
       cookies=TestWithdraw().login()  #获取到cookies值
       resp=request.requests(case['method'],case['url'],case['data'],cookies=cookies)  #调用requests并发送请求
       try:
           if resp.json()['msg']=='取现成功':
               logger.info('走数据校验分支')
               sql="SELECT LeaveAmount from future.member WHERE MobilePhone='15900002100'"
               results_after=MySqlMetul(return_dict=True).fetch_all(sql)[0]['LeaveAmount'] # 从数据库获取提现之后的余额
               results_after=Decimal(results_after).quantize(Decimal("0.00")) #提现之后的金额，设置保留两位小数并设置数据类型为十进制
               logger.info('提现之后的余额', results_after)
               import json
               case['data']=json.loads(case['data'])
               case['data']['amount']=Decimal(case['data']['amount']).quantize(Decimal("0.00")) #提现金额，设置保留两位小数并设置数据类型为十进制
               logger.info('提现金额',case['data']['amount'])
               pre_results=Decimal(self.pre_results).quantize(Decimal("0.00")) #提现之前的金额
               logger.info(type(pre_results))
               resx=results_after+case['data']['amount'] #提现之后的金额加上提现金额
               self.assertEqual(resx,self.pre_results) #断言
           else:
               logger.info('未走数据校验分支！')

           code=resp.json()['code']
           self.assertEqual(case['expected'],int(code)) #断言
           DoExcel(concant.excel_dir, 'withdraw').write_data(case['case_id']+1,7,code) #将响应返回的值回写表格中
           DoExcel(concant.excel_dir, 'withdraw').write_data(case['case_id']+1, 8,'Pass')
       except AssertionError as e:
           logger.info('断言报错了{}'.format(e))
           DoExcel(concant.excel_dir, 'withdraw').write_data(case['case_id']+1,7,code)
           DoExcel(concant.excel_dir, 'withdraw').write_data(case['case_id']+1, 8,'False')
           raise e  #抛出异常


if __name__ == '__main__':
    unittest.main()



