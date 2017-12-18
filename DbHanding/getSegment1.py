#coding=gbk

#对paragraph表中的原告诉称、被告辩称和查明事实段使用结巴进行分词
#将内容存入segment2表
#document格式
# {
#     _id(objectId)
#     text(string)原文字段
#     token(string)分词结果字段，空格隔开
#     flag(string)词性标注字段，空格隔开
#     keywords(string)关键词字段，空格隔开
#     tfidfsrc(stirng)计算tfidf值使用的数据
# }


import pymongo
from bson.objectid import ObjectId
from jieba import analyse, posseg
import re

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='getSegment.log',
                filemode='w')

textrank = analyse.textrank
analyse.set_stop_words("stopWords.txt")

def getFromMongo(col, fromId):

    nextId = fromId
    tag = 1

    res = list()

    condition = {} if fromId == "0" else {'_id': {'$gt': ObjectId(fromId)}}

    logging.info('This is info message')
    print(col.find(condition).limit(10000).count())
    if col.find(condition).limit(10000).count() == 0:
        tag = 0

    i = 1
    for item in col.find(condition).limit(10000):
        nextId = item["_id"]

        plaintiffAlleges = item['plaintiffAlleges']
        if isinstance(plaintiffAlleges, dict):
            if re.match(r'[0-9a-zA-Z]+', plaintiffAlleges['text']) == None:
                res.append({'text':plaintiffAlleges['text'], '_id':plaintiffAlleges['segmentid']})

        defendantArgued = item['defendantArgued']
        if isinstance(defendantArgued, dict):
            if re.match(r'[0-9a-zA-Z]+', defendantArgued['text']) == None:
                res.append({'text': defendantArgued['text'], '_id': defendantArgued['segmentid']})

        factFound = item['factFound']
        if isinstance(factFound, dict):
            if re.match(r'[0-9a-zA-Z]+', factFound['text']) == None:
                res.append({'text': factFound['text'], '_id': factFound['segmentid']})

        print(i)
        i+=1

    return (nextId, tag, res)


def handledata(res):
    i = 1
    for item in res:
        print(i, item)
        token, flag, keywords, tfidfSrc = tokenP(item['text'])
        item['token'] = token
        item['flag'] = flag
        item['keywords'] = keywords
        item['tfidfSrc'] = tfidfSrc
        print(item)
        i += 1
    return res


def tokenP(paragraph):
    tokenRes = list()
    flagRes = list()
    tfidfSrc = list()

    for word,flag in posseg.cut(paragraph):
        tokenRes.append(word)
        flagRes.append(flag)

    filterFlag = ('n', 'nz', 'nt', 'nl', 'ng', 'v', 'vd', 'vn', 'vi', 'vl', 'vg', 'v', 'vn', 'an', 'b', 'bl', 'd')
    keywordsRes = textrank(paragraph,topK=200,allowPOS=filterFlag)

    for item in tokenRes:
        if item in keywordsRes:
            tfidfSrc.append(item)

    return ((' ').join(tokenRes), (' ').join(flagRes), (' ').join(keywordsRes), (' ').join(tfidfSrc),)



def save2mongo(col, res):
    for item in res:
        col.insert(item)

if __name__ == '__main__':
    #连接数据库
    con = pymongo.MongoClient('localhost', 27017)
    col1 = con.Lawcase.paragraph
    col2 = con.Lawcase.segment2

    nextId = "0"

    i = 1
    while True:
        logging.info("第 %s 次读数据" % str(i))
        (nextId, tag, getRes) = getFromMongo(col1, nextId)
        logging.info("nextId： %s" % str(nextId))
        logging.info("enter token!")
        afterHadle = handledata(getRes)
        logging.info("exit token!")
        logging.info("exit save!")
        save2mongo(col2, afterHadle)
        logging.info("exit save!")
        i += 1

        if tag == 0:
            break
