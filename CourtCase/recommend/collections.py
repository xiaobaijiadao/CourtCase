import pymongo
from bson.objectid import ObjectId
from django.conf import settings


class indexTable:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase.indexTable

    def getCaselistByKeyforkeyword(self, word):
        res = dict()
        for item in self.col.find({"key": word}):
            for case in item["caselist"]:
                cs = dict()
                cs["tfidf"] = case["tfidf"]
                cs["wordsCount"] = 1
                res[case["caseid"]] = cs
        return res

    def getCaselistByKeyfortfidf(self, word):
        res = dict()
        for item in self.col.find({"key" : word}):
            for case in item["caselist"]:
                res[case["caseid"]] = case["tfidf"]
        return res


class LDAvec:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase.LDAvec

    def getCaselistByDis(self, dis):
        res = list()
        cond = dict()

        i = 0
        for d in dis:
            key = 'dis.'+str(i)
            if d != 0.0:
                cond[key] = {
                    '$gt': d - 0.3,
                    '$lt': d + 0.3,
                }
            else:
                cond[key] = {
                    '$lt': d + 0.3,
                }
            i += 1

        for item in self.col.find(cond):
            cs = dict()
            cs["id"] = item["fullTextId"]
            cs["dis"] = item['dis']
            res.append(cs)

        return res


class paragraph:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase.AJsegment

    def getInfo(self, id):
        item = self.col.find_one({"_id" : ObjectId(id)})
        return (item['fulltextid'], item['title'])

    def getInfoByFullTextId(self, id):
        item = self.col.find_one({"fulltextid": id})
        return (item['fulltextid'], item['title'])


class AJsegment:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase.AJsegment

    def getfulltextid(self, id):
        item = self.col.find_one({"_id" : ObjectId(id)})
        return item['fulltextid']


class lawcase:
    def __init__(self):
        self.col = settings.DB_CON.lawCase.lawcase

    def getInfo(self, id):
        item = self.col.find_one({"_id" : ObjectId(id)})
        return item['text']

class dispute:
    def __init__(self):
        self.col = settings.DB_CON.lawCase.tokendispute

    def getAllWeight(self):
        res = dict()
        for item in self.col.find():
            res[item["word"]] = item["weight"]

        return res

class searchPerform:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase.searchPerform

    def getReferenceNum(self):
        refNum = [len(item['ref']) for item in self.col.find()]
        return refNum

    def getRNAndCC(self, option):
        refNum = []
        coverCount = []

        cur = self.col.find(no_cursor_timeout = True)
        for item in cur:
            rn = []
            cc = []
            for i in item[option]:
                rn.append(len(i['ref']))
                cc.append(i['covercount'])
            refNum.append(rn)
            coverCount.append(cc)
        cur.close()

        return refNum,coverCount

    def getReferenceNumAndCoverCount(self):
        res = dict()

        res['ReferenceNumByKeyword'],res['CoverCountByKeyword'] = self.getRNAndCC('resByKeyWord')
        res['ReferenceNumByTfidf'],res['CoverCountByTfidf'] = self.getRNAndCC('resByTfidf')
        res['ReferenceNumByLda'],res['CoverCountByLda'] = self.getRNAndCC('resByLda')

        return res

    def getStatuteSetList(self, option, limit=50):
        #获取不同方法得到的50条数据中前10条，前20条和前50条的法条集合
        statuteSetList = []

        cur = self.col.find(no_cursor_timeout=True)

        if option == 'ref':
            for item in cur:
                statutes = set(item['ref'])
                statuteSetList.append(statutes)
        elif option == 'resByKeyWord' or option == 'resByTfidf' or option == 'resByLda':
            for item in cur:
                statutes = []
                for i in item[option][:limit]:
                    statutes.extend(i['ref'])

                statuteSetList.append(set(statutes))

        cur.close()

        return statuteSetList
