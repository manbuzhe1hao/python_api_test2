import os

base_dir=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
datas_dir=os.path.join(base_dir,'datas')
excel_dir=os.path.join(datas_dir,'py_data.xlsx')  #拼接测试案例的绝对路径
conf_dir=os.path.join(base_dir,'conf')
test1_dir=os.path.join(conf_dir,'test1.conf')
test2_dir=os.path.join(conf_dir,'test2.conf')
global_dir=os.path.join(conf_dir,'global.conf')
logs_dir=os.path.join(base_dir,'logs')
testcases_dir=os.path.join(base_dir,'testcases')
reports_dir=os.path.join(base_dir,'reports')
reports_html_dir=os.path.join(reports_dir,'reports_html.html')




