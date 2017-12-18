#coding=gbk
import pymongo, re
import jieba.posseg as pseg
import math

def getFromMongo(col):
    dic = dict()
    dic["all"] = 0
    dic["flag"] = list()

    for item in col1.find():
        token = list()
        for word, flag in pseg.cut(item["causeofaction"]):
            if re.search(r'[0-9a-zA-Z 、]', word) == None and len(word) != 1:
                token.append((word, flag))
                dic["flag"].append(flag)

        i = 1
        lenth = len(token)
        for item in token:
            if item[1] not in ['n', 'nr', 'nz', 'nt', 'v', 'vn', 'an']:
                continue
            if item[0] not in dic:
                dic[item[0]] = [(float(i / lenth), item[1]), ]
            else:
                dic[item[0]].append((float(i / lenth), item[1]))
            i += 1

        dic["all"] += 1

    return dic


def write2TokenDispute(col, dic):
    for word, caList in dic.items():
        if word != "all" and word != "flag":
            idf = math.log(len(caList)/dic["all"])
            posSum = 0
            for item in caList:
                posSum += item[0]

            pos = posSum/len(caList)
            posWeight = 0.6 if pos <= 0.5 else 0.4
            flagWeight = 0.7 if caList[0][1] in ['n', 'nr', 'nz', 'nt'] else 0.3

            weight = -idf * posWeight * flagWeight + 1
            doc = dict()
            doc["word"] = word
            doc["list"] = caList
            doc["weight"] = weight
            if weight > max:
                max = weight
            if weight < min:
                min = weight

            col.insert(doc)

if __name__ == '__main__':
    #连接数据库
    con = pymongo.MongoClient('localhost', 27017)
    col1 = con.Lawcase.codeofca
    col2 = con.Lawcase.tokendispute

    dic = getFromMongo(col1)

    write2TokenDispute(col2, dic)
