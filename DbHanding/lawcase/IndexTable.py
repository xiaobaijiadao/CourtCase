# coding:utf-8

# version1
# 输入：id,[key->tfidf]...
# 索引表 key,[id->tfidf]...

# version2
# 索引表 key->[(id,times),]->[pos,]
# eg:    key->[(1,2)(4,1)]->[2,7,1]

import pymongo, re
from bson import ObjectId
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='indexTable.log',
                filemode='w')


#stopwords = {}.fromkeys([line.rstrip() for line in open('stopWords.txt')])

def getDataFromMongo(col, fromId):
    nextId = fromId
    tag = 1

    condition = {} if fromId == "0" else {'_id': {'$gt': ObjectId(fromId)}}

    print(col.find(condition).limit(12000).count())
    if col.find(condition).limit(12000).count() == 0:
        tag = 0


    indexDict = dict()

    condition = {} if fromId == "0" else {'_id': {'$gt': ObjectId(fromId)}}

    i = 1
    for item in col.find(condition).limit(12000):
        #print(i, item)
        nextId = item["_id"]
        for wt in item["wordslist"]:#v -> [{"word": , "tfidf": },...]
            if wt["word"] in indexDict:
                indexDict[wt["word"]]["caselist"].append({"caseid":item["lawcaseid"], "tfidf":wt["tfidf"]})
            else:
                dic = dict()
                dic["key"] = wt["word"]
                caselist = list()
                caselist.append({"caseid":item["lawcaseid"], "tfidf":wt["tfidf"]})
                dic["caselist"] = caselist
                indexDict[wt["word"]] = dic
        i += 1

    return (indexDict, nextId, tag)


def write2mongo(col, indexDict):
    i = 1
    lenth = len(indexDict)
    for k,v in indexDict.items():
        print("w", i, lenth, len(v["caselist"]))
        col.insert(v)
        #res = col.find_one({'key':k})
        #print(res, v)
        # if res is None:
        #     col.insert(v)
        # else:
        #     # for item in v["caselist"]:
        #     #     res["caselist"].append(item)
        #     # col.update({'key':k}, res)
        #     col.update({"key": k}, {"$addToSet": {"caselist": {"$each": v["caselist"]}}})
        i += 1


if __name__ == '__main__':
    # 连接数据库
    con = pymongo.MongoClient('192.168.68.11', 20000)
    #con = pymongo.MongoClient('localhost', 27017)
    col1 = con.divorceCase.tf_idf
    col2 = con.divorceCase.indexTable

    nextId = "0"

    i = 1
    while True:
        logging.info("第 %s 次读数据" % str(i))
        logging.info("enter read!")
        (indexDict, nextId, tag) = getDataFromMongo(col1, nextId)
        logging.info("nextId： %s" % str(nextId))
        logging.info("enter write!")
        write2mongo(col2, indexDict)
        i += 1

        if tag == 0:
            break

    logging.info("finish!")