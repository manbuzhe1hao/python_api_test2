import logging
import logging.handlers
from common import concant
import os
def getloging(name):
    getloging=logging.getLogger(name) #创建日志收集容器
    getloging.setLevel('INFO') #设计收集级别
    formatter=logging.Formatter('[%(levelno)s]-[%(filename)s]-[%(asctime)s]-[%(message)s]')

    ch=logging.StreamHandler() #创建输出控制台渠道
    ch.setLevel('INFO') #设置输出渠道
    ch.setFormatter(formatter) #设置输出格式

    filename=os.path.join(concant.logs_dir,'case.logs') #设置输出日志的绝对路径
    fh=logging.handlers.RotatingFileHandler(filename,encoding='utf-8',maxBytes=1024*1024, backupCount=10) #配置文件输出渠道
    fh.setLevel('INFO')
    fh.setFormatter(formatter)

    getloging.addHandler(ch) #对接
    getloging.addHandler(fh)
    return getloging



    
