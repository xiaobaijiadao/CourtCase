import pymongo
from bson.objectid import ObjectId
from django.conf import settings


class indexTable:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase3.indexTable

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
        self.col = settings.DB_CON.divorceCase3.LDAvec

    def getCaselistByDis(self, dis):
        res = list()
        cond = dict()

        i = 0
        for d in dis:
            key = 'vec.'+str(i)
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
            cs["vec"] = item['vec']
            res.append(cs)

        return res

    def getCaselistByDisAndDirect(self, dis, direct):
        res = list()
        cond = dict()

        cond['dis'] = {
            '$gt': dis - 0.5,
            '$lt': dis + 0.5,
        }
        cond['direct'] = {
            '$gt': direct - 0.05,
            '$lt': direct + 0.05,
        }

        for item in self.col.find(cond):
            cs = dict()
            cs["id"] = item["fullTextId"]
            cs["vec"] = item['vec']
            res.append(cs)

        return res

    def getCaselistByTopic(self, topic, d):
        res = list()
        cond = dict()
        key = 'vec.' + str(topic)
        cond['topic'] = {
            '$gt': d - 0.15,
            '$lt': d + 0.15,
        }

        for item in self.col.find(cond):
            cs = dict()
            cs["id"] = item["fullTextId"]
            res.append(cs)

        return res


class paragraph:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase3.databaseAJsegment

    def getInfo(self, id):
        item = self.col.find_one({"_id" : ObjectId(id)})
        return (item['fulltextid'], item['title'])

    def getInfoByFullTextId(self, id):
        item = self.col.find_one({"fulltextid": id})
        return (item['fulltextid'], item['title'])


class AJsegment:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase3.databaseAJsegment

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

class searchPerformTest:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase3.searchPerform

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


class searchEvaluate:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase3.searchPerformEvaluate

    def getRateByName(self, limit, tag):
        res = []
        for item in self.col.find_one({"name" : name, "tag": tag})['method']:
            res.append(item['value'])
        return res

    def getMeanRateByName(self, name, tag):
        res = []
        for item in self.col.find_one({"name" : name, "tag": tag})['method']:
            res.append(item['meanValue'])
        return res

    def getAllRateByName(self, name, tag):
        res = []
        for item in self.col.find_one({"name" : name, "tag": tag})['method']:
            res.append(item['allValue'])
        return res


class searchResEvaluate:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase3.searchResEvaluate
        self.limit = ['1', '3', '5', '10', '20', '50']

    def getPrecisionAndName(self, tag, limit):
        res = {
            'tName' : [],
            'sortPrecisionList' : [],
            'sortRecallList' : [],
            'sortF1List' : [],
            'noSortPrecisionList' : [],
            'noSortRecallList' : [],
            'noSortF1List' : [],
        }

        if limit not in self.limit:
            return None

        cur = self.col.find({'tag': tag}, no_cursor_timeout = True)
        index = self.limit.index(limit)
        for item in cur:
            res['tName'].append(item['tname'])
            res['sortPrecisionList'].append(item['sortP'][index])
            res['sortRecallList'].append(item['sortR'][index])
            res['sortF1List'].append(item['sortF'][index])
            res['noSortPrecisionList'].append(item['nosortP'][index])
            res['noSortRecallList'].append(item['nosortR'][index])
            res['noSortF1List'].append(item['nosortF'][index])
        cur.close()

        return res


class searchStatuteEvaluate:
    def __init__(self):
        self.col = settings.DB_CON.divorceCase3.searchStatutePerformValidateEvaluate

    def getRateByName(self, option):
        if option not in ['precision', 'recall', 'f-measure']:
            print("option error!")
            return None

        res = [[], [], [], []]
        i = 0
        for item in self.col.find():
            res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount5'])
            res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount10'])
            res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount20'])
            res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount50'])
            res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount5'])
            res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount10'])
            res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount20'])
            res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount50'])
            res[i * 2].append(item[option]['resStaByLda']['simple']['covercount5'])
            res[i * 2].append(item[option]['resStaByLda']['simple']['covercount10'])
            res[i * 2].append(item[option]['resStaByLda']['simple']['covercount20'])
            res[i * 2].append(item[option]['resStaByLda']['simple']['covercount50'])
            res[i * 2].append(item[option]['resStaByTest']['simple']['covercount5'])
            res[i * 2].append(item[option]['resStaByTest']['simple']['covercount10'])
            res[i * 2].append(item[option]['resStaByTest']['simple']['covercount20'])
            res[i * 2].append(item[option]['resStaByTest']['simple']['covercount50'])

            res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount5'])
            res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount10'])
            res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount20'])
            res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount50'])
            res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount5'])
            res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount10'])
            res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount20'])
            res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount50'])
            res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount5'])
            res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount10'])
            res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount20'])
            res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount50'])
            res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount5'])
            res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount10'])
            res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount20'])
            res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount50'])
            i += 1
        return res