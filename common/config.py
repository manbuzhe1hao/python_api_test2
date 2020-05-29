from common import concant
from configparser import ConfigParser

class ReadConfig:
    def __init__(self):
        self.config=ConfigParser()  #实例化对象
        self.config.read(concant.global_dir) #读取数据
        retult=self.config.getboolean('switch','open')
        if retult:
            self.config.read(concant.test1_dir)
        else:
            self.config.read(concant.test2_dir)
    def get(self,section,option):
        return self.config.get(section,option)





