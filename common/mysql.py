import pymysql
class MySqlMetul:
    def __init__(self,return_dict=False): #初始化函数，建立连接
        #想想这块如何做到配置文件里面去？？
        host='test.lemonban.com'
        user='test'
        password='test'
        #建立连接
        self.connect=pymysql.connect(host=host,user=user,password=password,port=3306) #连接数据库
        #新建一个查询
        if return_dict:
            self.cursor=self.connect.cursor(pymysql.cursors.DictCursor) #指定每行数据以字典的形式返回
        else:
            self.cursor=self.connect.cursor() #指定每行数据以元组的形式返回
    def fetch_one(self,sql): #执行sql语句，返回一条数据，返回的数据类型是元组
        self.cursor.execute(sql) #执行sql语句
        result=self.cursor.fetchone() #查询结果
        return result
    def fetch_all(self,sql): #执行sql语句，返回多条数据 ->返回的数据类型为列表，列表里面嵌套元组[(),()]-->取值不方便
        self.cursor.execute(sql)
        reslut=self.cursor.fetchall()
        return reslut
    def close(self): #关闭
        self.cursor.close() #关闭连接
        self.connect.close() #关闭数据库

if __name__ == '__main__':
    mysql=MySqlMetul(return_dict=True)
    sql="select * from future.member where mobilephone=13999999831"
    results=mysql.fetch_all(sql)#返回的是列表里面放字典
    print(results)
    print(type(results))
    for result in results:
        print(result)
    mysql.close()



