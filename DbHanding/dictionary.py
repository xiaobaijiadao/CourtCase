#coding=gbk

#对AJsegment表中的ladsrc中词汇建立dictionary表
#将内容存入segment2表
#document格式
# {
#     _id(objectId)
#     word(string)词
#     pos(int)向量位置
# }


import pymongo
from bson.objectid import ObjectId

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dictionary.log',
                filemode='w')


def getFromMongo(col, fromId):

    nextId = fromId
    tag = 1

    res = list()

    condition = {} if fromId == "0" else {'_id': {'$gt': ObjectId(fromId)}}

    logging.info('This is info message')
    print(col.find(condition).limit(2000).count())
    if col.find(condition).limit(2000).count() == 0:
        tag = 0

    cur = col.find(condition, no_cursor_timeout = True).limit(2000)
    for item in cur:
        res.extend(item['ldasrc'].strip().split(' '))
        nextId = item["_id"]

    cur.close()

    return (nextId, tag, set(res))


def handledata(res, col):
    result = list()
    fromPos = col.count()
    i = fromPos

    if '' in res:
        res.remove('')

    if i == 0:
        for item in res:
            result.append({
                "word": item,
                "pos": i,
            })
            i += 1
    else:
        for item in res:
            if col.find({"word" : item}) == None:
                result.append({
                    "word" : item,
                    "pos" : i,
                })
                i += 1

    logging.info("本次写入： %d 条" % i)
    return result


def save2mongo(col, res):
    for item in res:
        col.insert(item)

if __name__ == '__main__':
    #连接数据库
    con = pymongo.MongoClient('localhost', 27017)
    col1 = con.Lawcase.AJsegment
    col2 = con.Lawcase.dictionary
    # con = pymongo.MongoClient('192.168.68.11', 20000)
    # col1 = con.lawCase.AJsegment
    # col2 = con.lawCase.dictionary

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
        save2mongo(col2, afterHadle)
        logging.info("exit save!")
        i += 1

        if tag == 0:
            break