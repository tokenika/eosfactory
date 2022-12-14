import configparser
import os
conf = configparser.RawConfigParser()
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf.read(root_path + '/config.ini','utf8')

def readconf(section,option):
    return conf.get(section=section,option=option)