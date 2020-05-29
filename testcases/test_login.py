from common import concant
from common.do_excel import DoExcel
import unittest
from common.request import Requests
from ddt import ddt,data
from common.logger import getloging
do_excel= DoExcel(concant.excel_dir, 'login').get_data() #读取excel的值
request=Requests() #实例化requests请求
logger=getloging('login')
@ddt
class TestLogin(unittest.TestCase): #继承unittest.TestCase


    @data(*do_excel) #引入ddt
    def test_login(self,case):
       logger.info('开始执行{}条测试用例'.format(case['case_id']))
       resp=request.requests(case['method'],case['url'],case['data'])  #调用requests并发送请求
       try:
           self.assertEqual(case['expected'],resp.text) #断言
           DoExcel(concant.excel_dir, 'login').write_data(case['case_id']+1,7,resp.text) #将响应返回的值回写表格中
           DoExcel(concant.excel_dir, 'login').write_data(case['case_id']+1, 8,'Pass')
       except AssertionError as e:
           logger.info('断言报错了{}'.format(e))
           DoExcel(concant.excel_dir, 'login').write_data(case['case_id']+1,7,resp.text)
           DoExcel(concant.excel_dir, 'login').write_data(case['case_id']+1, 8,'False')
           raise e  #抛出异常


if __name__ == '__main__':
    unittest.main()



