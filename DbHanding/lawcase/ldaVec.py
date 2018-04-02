import pymongo
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='ldaVec.log',
                filemode='w')

def getData(col):
    items = []
    for i in col.find().limit(18000):
        item = {}
        item['fullId'] = i['fullTextId']
        item['vec'] = i['dis']
        item['topic'] = i['dis'].index(max(i['dis']))
        items.append(item)
    return items

def computeDisAndDirect(vec):
    mod = np.ones((len(vec)))*5
    vec = np.array(vec)*10
    dis = np.linalg.norm(vec-mod)

    Lm = np.sqrt(mod.dot(mod))
    Lv = np.sqrt(vec.dot(vec))
    direc = vec.dot(mod)/(Lm*Lv)

    return dis, direc

def write2Mongo(col, items):
    for i in items:
        col.insert(i)


if __name__ == '__main__':
    con = pymongo.MongoClient('192.168.68.11', 20000)
    col1 = con.divorceCase3.LDAvec
    col2 = con.divorceCase3.LDAvec2

    items = getData(col1)
    dismin = 100
    dismax = 0
    dirmin = 100
    dirmax = 0
    for item in items:
        item['dis'], item['direct'] = computeDisAndDirect(item['vec'])
        if item['dis'] > dismax:
            dismax = item['dis']
        if item['dis'] < dismin:
            dismin = item['dis']
        if item['direct'] > dirmax:
            dirmax = item['direct']
        if item['direct'] < dirmin:
            dirmin = item['direct']
    write2Mongo(col2, items)
    logging.info("mindis：%f" % dismin)
    logging.info("maxdis：%f" % dismax)
    logging.info("mindir：%f" % dirmin)
    logging.info("maxdir：%f" % dirmax)