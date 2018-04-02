import pymongo, sys
import numpy as np

class statutePerform():

    def __init__(self, col1, col2, tag, name):
        self.col1 = col1
        self.col2 = col2
        self.tag = tag
        self.name = name
        self.getDataFromDB(tag)

    def getDataFromDB(self, tag):
        srcStatuteList = []
        searchStatuteList = []

        cur = self.col1.find({"tag": tag}, no_cursor_timeout=True)
        for item in cur:
            srcStatuteList.append(set(item['ref']))
            statutes = [(i['ref'], i['sim2']) for i in item['res']]
            searchStatuteList.append(statutes)
        cur.close()
        self.srcStatuteList = srcStatuteList
        self.searchStatuteList = searchStatuteList

    def getStatuteSetList(self, limit, presort=False):
        #获取不同方法得到的50条数据中top1,top3,top5,top10,top20,top50的法条集合
        statuteSetList = []
        for item in self.searchStatuteList:
            sortList = None
            if not presort:
                sortList = item[:limit]
            else:
                sortList = sorted(item, key=lambda item: item[1], reverse=True)[:limit]
            statutes = []
            for item in sortList:
                statutes.extend(item[0])
            statuteSetList.append(set(statutes))
        return statuteSetList

    def getcoverCount(self, refset1, refset2):
        #refset1为标准法条引用集合
        #refset2为搜索结果的法条引用集合
        count = len(set(refset1) & set(refset2))
        return count

    def genPrecisionAndRecallAndF1(self, refsetList1, refsetList2):
        # refsetlist1为标准法条引用集合
        # refsetlist2为搜索结果的法条引用集合
        precisionList = []
        recallList = []
        f1List = []

        for refset1, refset2 in zip(refsetList1, refsetList2):

            coverCount = self.getcoverCount(refset1, refset2)

            if len(refset2) != 0:
                p = round(coverCount / len(refset2), 3)
            else:
                p = 0
            if len(refset1) != 0:
                r = round(coverCount / len(refset1), 3)
            else:
                r = 0
            f1 = round(2*p*r / (p+r), 3) if p+r != 0 else 0

            precisionList.append(p)
            recallList.append(r)
            f1List.append(f1)

        res = (round(np.mean(np.array(precisionList)), 3), \
               round(np.mean(np.array(recallList)), 3), \
               round(np.mean(np.array(f1List)), 3))

        return res

    def genEvaluate(self):
        result = {}
        result['tname'] = self.name
        result['tag'] = self.tag
        result['nosortP'] = []
        result['sortP'] = []
        result['nosortR'] = []
        result['sortR'] = []
        result['nosortF'] = []
        result['sortF'] = []
        for i in [1, 3, 5, 10, 20, 50]:
            searchStatuteSetList = self.getStatuteSetList(i, presort=False)
            sortSearchStatuteSetList = self.getStatuteSetList(i, presort=True)

            nosortPrecision, nosortRecall, nosortF1 = self.genPrecisionAndRecallAndF1(self.srcStatuteList, searchStatuteSetList)
            sortPrecision, sortRecall, sortF1 = self.genPrecisionAndRecallAndF1(self.srcStatuteList, sortSearchStatuteSetList)
            result['nosortP'].append(nosortPrecision)
            result['sortP'].append(sortPrecision)
            result['nosortR'].append(nosortRecall)
            result['sortR'].append(sortRecall)
            result['nosortF'].append(nosortF1)
            result['sortF'].append(sortF1)

        self.col2.insert(result)


if __name__ == '__main__':
    con = pymongo.MongoClient('192.168.68.11', 20000)
    col1list = [
        (con.divorceCase3.searchResLdaTopic, 'ldaTopic'),
        (con.divorceCase3.searchResTfidf, 'tfidf'),
        (con.divorceCase3.searchResWeightTfidf, 'weightTfidf'),
        (con.divorceCase3.searchResLdaVec, 'ldaVec'),
        (con.divorceCase3.searchResLdaDisDirect, 'ldaDisDirect'),
        (con.divorceCase3.searchResLdaAll, 'ldaAll'),
        (con.divorceCase3.searchResDoc2vec, 'doc2vec'),
    ]
    col2 = con.divorceCase3.searchResEvaluate
    for col1 in col1list:
        for tag in ['2', '3', '4']:
            sp = statutePerform(col1[0], col2, tag, col1[1])
            sp.genEvaluate()