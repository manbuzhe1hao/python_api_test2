import unittest
from libex import HTMLTestRunnerNew
from common import concant

discover=unittest.defaultTestLoader.discover(concant.testcases_dir, pattern='test_*.py',top_level_dir=None)
with open(concant.reports_html_dir,'wb+') as file:
    runner=HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                            verbosity=2,
                                            title='python_api_02',
                                            description='加油加油！',
                                            tester='漫步者1号')
    runner.run(discover)


