# encoding=utf-8

#构建最原始的mongodb数据库,暂时只有46条测试数据，用于django框架测试连接mongodb

import pymongo

import os
import os.path

from xml.sax.handler import ContentHandler
from xml.sax import parse

cases = []

class TestHandler(ContentHandler):

    def startElement(self, name, attrs):
        if name == 'AYDM' or name == 'QW' or name == 'title' or name == 'FYCJM' or name == 'YGSCD' or name == 'BGBCD' or name == 'CMSSD' or name == 'CUS_JANYR':
            print(attrs['value'])
            self.case[name] = attrs['value']

    def endElement(self, name):
        if name == 'writ':
            cases.append(self.case)

if __name__ == "__main__":
    con = pymongo.MongoClient()
    col = con.caseTest.allCase

    dirname = "/Users/wangxiao/Desktop/Cases"
    for parent, dirnames, filenames in os.walk(dirname):
        for file in filenames:
            if file.endswith('.xml'):
                print(file)
                th = TestHandler()
                th.case = {}
                parse(os.path.join(parent,file), th)

    for c in cases:
        col.insert(c)