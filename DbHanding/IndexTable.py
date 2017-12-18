# coding:utf-8

# version1
# 输入：id,[key->tfidf]...
# 索引表 key,[id->tfidf]...

# version2
# 索引表 key->[(id,times),]->[pos,]
# eg:    key->[(1,2)(4,1)]->[2,7,1]

import pymongo, re
from bson import ObjectId


stopwords = {}.fromkeys([line.rstrip() for line in open('stopWords.txt')])

def getDataFromMongo(col, fromId):
    nextId = fromId
    tag = 1

    condition = {} if fromId == "0" else {'_id': {'$gt': ObjectId(fromId)}}

    print(col.find(condition).limit(10000).count())
    if col.find(condition).limit(10000).count() == 0:
        tag = 0


    indexDict = dict()

    condition = {} if fromId == "0" else {'_id': {'$gt': ObjectId(fromId)}}

    i = 1
    for item in col.find(condition).limit(10000):
        print(i, item)
        nextId = item["_id"]
        for wt in item["wordslist"]:#v -> [{"word": , "tfidf": },...]
            if wt["word"] not in stopwords and re.search(r'[0-9a-zA-Z ]+', wt["word"]) == None and len(wt["word"]) >1:
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
        print("w", i, lenth)
        res = col.find_one({'key':k})
        print(res, v)
        if res is None:
            col.insert(v)
        else:
            # for item in v["caselist"]:
            #     res["caselist"].append(item)
            # col.update({'key':k}, res)
            col.update({"key": k}, {"$addToSet": {"caselist": {"$each": v["caselist"]}}})
        i += 1


if __name__ == '__main__':
    # 连接数据库
    con = pymongo.MongoClient('localhost', 27017)
    col1 = con.Lawcase.tf_idf
    col2 = con.Lawcase.indexTable2

    nextId = "0"

    while True:
        (indexDict, nextId, tag) = getDataFromMongo(col1, nextId)
        write2mongo(col2, indexDict)

        if tag == 0:
            break
