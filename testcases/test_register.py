from common import concant
from common.do_excel import DoExcel
import unittest
from common.request import Requests
from ddt import ddt,data
from common.mysql import MySqlMetul
from common.logger import getloging
logger=getloging('register')

do_excel= DoExcel(concant.excel_dir, 'register').get_data() #读取excel的值
request=Requests() #实例化requests请求

@ddt
class TestRegister(unittest.TestCase): #继承unittest.TestCase
    def setUp(self):
        self.mysql = MySqlMetul(return_dict=True)  # 实例化封装的mysql,每执行一条案例就实例化一次
        sql = "select max(MobilePhone)  as max_phone from future.member WHERE MobilePhone LIKE '139%'"
        self.max_mobile = self.mysql.fetch_one(sql)['max_phone']  # 取到数据库中最大的值
    @data(*do_excel) #引入ddt
    def test_register(self,case):
       logger.info('开始执行{}条用例'.format(case['case_id']))
       import json
       case['data']=json.loads(case['data']) #将字符串转换成字典类型
       if case['data']['mobilephone']=="${mobile_phone}": #判断测试用例中是否存在"${mobile_phone}"
           case['data']['mobilephone'] = int(self.max_mobile)+1 #数据库中最大的值+1，并赋值
       resp=request.requests(case['method'],case['url'],case['data'])  #调用requests并发送请求
       try:
           self.assertEqual(case['expected'],resp.text) #断言
           if resp.json()['msg']=='注册成功': #msg信息注册成功，这判断数据校验
               sql="select * from future.member where mobilephone='{0}'".format(case['data']['mobilephone'])
               resutls=MySqlMetul(return_dict=True).fetch_all(sql)
               #首先判断是否有成功插入数据
               self.assertEqual(1,len(resutls)) #对比长度是否有值
               member=resutls[0] #获取到这一条数据，是一个字典
               self.assertEqual(0,member['LeaveAmount']) #判断注册成功余额应该是0
           DoExcel(concant.excel_dir, 'register').write_data(case['case_id']+1,7,resp.text) #将响应返回的值回写表格中
           DoExcel(concant.excel_dir, 'register').write_data(case['case_id']+1, 8,'Pass')
       except AssertionError as e:
           logger.info('断言报错了{}'.format(e))
           DoExcel(concant.excel_dir, 'register').write_data(case['case_id']+1,7,resp.text)
           DoExcel(concant.excel_dir, 'register').write_data(case['case_id']+1, 8,'False')
           raise e  #抛出异常
    def tearDown(self):
        self.mysql.close()


if __name__ == '__main__':
    unittest.main()



