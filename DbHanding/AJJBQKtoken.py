#coding=gbk

#结合paragraph表中全文id和原告诉称、被告辩称和查明事实段和segment表中的分词结果（tfidfsrc项）
#将合并的分词结果存入AJJBQKToken表中
#document格式
# {
#     _id(objectId)
#     fullTextId(String)
#     token(string)分词结果字段，空格隔开
# }


import pymongo
from bson.objectid import ObjectId
import re

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='ajjbqk.log',
                filemode='w')

def getFromMongo(col, fromId):

    nextId = fromId
    tag = 1

    res = list()

    condition = {} if fromId == "0" else {'_id': {'$gt': ObjectId(fromId)}}

    logging.info('This is info message')
    if col.find(condition).limit(10000).count() == 0:
        tag = 0

    i = 1
    for item in col.find(condition).limit(10):
        nextId = item["_id"]

        doc = dict()
        doc['fullTextId'] = item['fullTextId']
        doc['idlist'] = list()
        plaintiffAlleges = item['plaintiffAlleges']
        if isinstance(plaintiffAlleges, dict):
            if re.match(r'[0-9a-zA-Z]+', plaintiffAlleges['text']) == None:
                doc['idlist'].append(item['plaintiffAlleges']['segmentid'])

        defendantArgued = item['defendantArgued']
        if isinstance(defendantArgued, dict):
            if re.match(r'[0-9a-zA-Z]+', defendantArgued['text']) == None:
                doc['idlist'].append(item['defendantArgued']['segmentid'])

        factFound = item['factFound']
        if isinstance(factFound, dict):
            if re.match(r'[0-9a-zA-Z]+', factFound['text']) == None:
                doc['idlist'].append(item['factFound']['segmentid'])

        res.append(doc)

        i+=1

    return (nextId, tag, res)


def handledata(res, col):
    result = list()

    for item in res:
        doc = dict()
        if len(item['idlist']) != 0:
            doc['fullTextId'] = item['fullTextId']
            token = list()
            flag = list()
            ldasrc = list()

            for id in item['idlist']:
                segment = col.find_one({'_id' : id})
                if segment == None:
                    logging.info("查找丢失：%s:%s" % (item['fullTextId'], id))
                    continue
                token.append(segment['token'])
                flag.append(segment['flag'])
                ldasrc.append(segment['tfidfSrc'])

            doc['token'] = ' '.join(token)
            doc['flag'] = ' '.join(flag)
            doc['ldasrc'] = ' '.join(ldasrc)
            result.append(doc)

    return result


def save2mongo(col, res):
    for item in res:
        col.insert(item)

if __name__ == '__main__':
    #连接数据库
    con = pymongo.MongoClient('192.168.68.11', 20000)
    col1 = con.lawCase.paragraph
    col2 = con.lawCase.segment2
    col3 = con.lawCase.AJJBQKToken

    nextId = "0"

    i = 1
    while True:
        logging.info("第 %s 次读数据" % str(i))
        (nextId, tag, getRes) = getFromMongo(col1, nextId)
        logging.info("nextId： %s" % str(nextId))
        logging.info("enter token!")
        afterHadle = handledata(getRes, col2)
        logging.info("exit token!")
        logging.info("exit save!")
        save2mongo(col3, afterHadle)
        logging.info("exit save!")
        i += 1

        if tag == 0:
            break