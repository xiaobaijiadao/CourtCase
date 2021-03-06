# 第一次：粗提取。
# 获取输入，进行分词，从索引表中提取出存在分词的案件的id
# 输入：从前端获取的字符串
# 输出：按tfidf值排序的id列表

import jieba
import numpy as np
from .collections import indexTable, dispute, LDAvec

from time import clock
from django.conf import settings

class roughExtract:
    def __init__(self, input):
        startSeg = clock()
        self.seg = list(jieba.cut_for_search(input))
        finishSeg = clock()
        print("分词耗时： %d 秒" % (finishSeg - startSeg))

    def getIndexListbykeyword(self):#通过tfidf获取查询结果
        indextb = indexTable()

        midResult1 = dict()

        # #所有包含关键字的案件的tfidf求和值和包含关键字总数

        for s in self.seg:
            for k,v in indextb.getCaselistByKeyforkeyword(s).items():
                if k not in midResult1:
                    case = dict()
                    case["tfidf"] = v["tfidf"]
                    case["wordsCount"] = 1
                    midResult1[k] = case
                else:
                    midResult1[k]["tfidf"] += v["tfidf"]
                    midResult1[k]["wordsCount"] += 1

        #首先按wordsCount归类
        midResult2 = dict()
        for k,v in midResult1.items():
            if v["wordsCount"] not in midResult2:
                cslist = list()
                cslist.append((k, v["tfidf"]))
                midResult2[v["wordsCount"]] = cslist
            else:
                midResult2[v["wordsCount"]].append((k, v["tfidf"]))
        #在同一个wordsCount下按tfidf排序
        for k,v in midResult2.items():
            midResult2[k] = sorted(v, key=lambda item: item[1],  reverse=True)

        #对wordsCount排序
        midResult3 = sorted(midResult2.items(), key=lambda item: item[0],  reverse=True)
        res = list()
        for item in midResult3:
            for i in item[1]:
                res.append(i[0])
                if len(res)>49:
                    print(len(res))
                    return res

        print(len(res))

        return res


    def getIndexListbytfidf(self):#通过加权tfidf获取查询结果
        indextb = indexTable()

        midResult = dict()

        keyWordsWeight = dispute().getAllWeight()

        #所有包含关键字的案件的tfidf求和值
        startReadMongo = clock()
        for s in self.seg:
            for caseid,tfidf in indextb.getCaselistByKeyfortfidf(s).items():
                weight = 1
                if s in keyWordsWeight:
                    weight = keyWordsWeight[s]
                if caseid not in midResult:
                    midResult[caseid] = tfidf * weight
                else:
                    midResult[caseid] += tfidf * weight

        finishReadMongo = clock()
        print("查询索引表时间：%d 微秒" % (finishReadMongo - startReadMongo))

        #对tfidf和排序
        startSort = clock()
        sortRes = sorted(midResult.items(), key=lambda item: item[1],  reverse=True)
        res = list()
        for item in sortRes:
            res.append(item[0])
            if len(res)>49:
                break
        finishSort = clock()
        print("排序时间：%d微秒" % (finishSort-startSort))
        print(len(res))

        return res


    def getIndexListbyLda(self, option = 1, ldamodel = '', text2vec = ''):#通过LDA获取查询结果
        ldavec = LDAvec()
        midres = list()

        #所有包含关键字的案件的tfidf求和值

        doc_bow = settings.TEXT2VEC.doc2bow(list(self.seg))  # 文档转换成bow
        doc_lda = settings.LDA_MODEL[doc_bow]  # 得到新文档的主题分布
        print(doc_lda)

        #将密集向量转化为稀疏向量
        topic_num = 6
        i = 0
        vec = list()
        for j in range(topic_num):
            if i < len(doc_lda):
                if doc_lda[i][0] == j:
                    vec.append(float(doc_lda[i][1]))
                    i += 1
                else:
                    vec.append(0.0)
            else:
                vec.append(0.0)

        items = []
        if option == 1:
            startReadMongo1 = clock()
            items = ldavec.getCaselistByDis(vec)
            finishReadMongo1 = clock()
            print("方式1查询LDA表时间：%d 微秒" % (finishReadMongo1 - startReadMongo1))
        elif option == 2:

            def computeDisAndDirect(vec):
                mod = np.ones((len(vec))) * 5
                vec = np.array(vec) * 10
                dis = np.linalg.norm(vec - mod)
                Lm = np.sqrt(mod.dot(mod))
                Lv = np.sqrt(vec.dot(vec))
                direc = vec.dot(mod) / (Lm * Lv)
                return dis, direc

            startReadMongo2 = clock()
            dis, direc = computeDisAndDirect(vec)
            items = ldavec.getCaselistByDisAndDirect(dis, direc)
            finishReadMongo2 = clock()
            print("方式2查询LDA表时间：%d 微秒" % (finishReadMongo2 - startReadMongo2))
        elif option == 3:
            d = max(vec)
            topic = vec.index(d)
            startReadMongo3 = clock()
            items = ldavec.getCaselistByDisAndDirect(topic, d)
            finishReadMongo3 = clock()
            print("方式3查询LDA表时间：%d 微秒" % (finishReadMongo3 - startReadMongo3))

        for item in items:
            gauseDis = 0.0
            for dis1, dis2 in zip(vec, item['dis']):
                gauseDis += abs(dis1-dis2)
            midres.append((item['id'], gauseDis))

        #对计算的lda相似度排序
        startSort = clock()
        res = sorted(midres, key=lambda item: item[1])[:50]
        res = [i[0] for i in res]

        finishSort = clock()
        print("排序时间：%d微秒" % (finishSort-startSort))
        print(len(res))

        return res

if __name__ == '__main__':
    pass

