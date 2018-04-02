# 第一次：粗提取。
# 获取输入，进行分词，从索引表中提取出存在分词的案件的id
# 输入：从前端获取的字符串
# 输出：按tfidf值排序的id列表

import jieba
import numpy as np
from . import collections as cs
from gensim import models, corpora

class roughExtract:
    def __init__(self, input, con):
        self.seg = list(jieba.cut_for_search(input))
        self.con = con

    def getIndexListbyTfidf(self):#通过tfidf获取查询结果
        indextb = cs.indexTable(self.con)
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
        midResult3 = sorted(midResult2.items(), key=lambda item: item[0],  reverse=True)[:50]
        res = [item[0] for item in midResult3]

        return res


    def getIndexListbyWeightTfidf(self):#通过加权tfidf获取查询结果
        indextb = cs.indexTable(self.con)

        midResult = dict()
        keyWordsWeight = cs.dispute(self.con).getAllWeight()

        #所有包含关键字的案件的tfidf求和值
        for s in self.seg:
            for caseid,tfidf in indextb.getCaselistByKeyfortfidf(s).items():
                weight = 1
                if s in keyWordsWeight:
                    weight = keyWordsWeight[s]
                if caseid not in midResult:
                    midResult[caseid] = tfidf * weight
                else:
                    midResult[caseid] += tfidf * weight

        #对tfidf和排序
        sortRes = sorted(midResult.items(), key=lambda item: item[1],  reverse=True)[:50]
        res = [item[0] for item in sortRes]

        return res


    def getIndexListbyLda(self, option, ldamodel, text2vec):#通过LDA获取查询结果
        ldavec = cs.LDAvec(self.con)
        midres = list()

        #所有包含关键字的案件的tfidf求和值

        doc_bow = text2vec.doc2bow(list(self.seg))  # 文档转换成bow
        doc_lda = ldamodel[doc_bow]  # 得到新文档的主题分布

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
            items = ldavec.getCaselistByDis(vec)
        elif option == 2:
            def computeDisAndDirect(vec):
                mod = np.ones((len(vec))) * 5
                vec = np.array(vec) * 10
                dis = np.linalg.norm(vec - mod)
                Lm = np.sqrt(mod.dot(mod))
                Lv = np.sqrt(vec.dot(vec))
                direc = vec.dot(mod) / (Lm * Lv)
                return dis, direc

            dis, direc = computeDisAndDirect(vec)
            items = ldavec.getCaselistByDisAndDirect(dis, direc)
        elif option == 3:
            d = max(vec)
            topic = vec.index(d)
            items = ldavec.getCaselistByTopic(topic, d)
        elif option == 4:
            d = max(vec)
            topic = vec.index(d)
            items = ldavec.getCaseList()

        for item in items:
            gauseDis = np.linalg.norm(np.array(vec) - np.array(item['vec']))
            midres.append((item['id'], gauseDis))

        #对计算的lda相似度排序
        res = sorted(midres, key=lambda item: item[1])[:50]
        res = [i[0] for i in res]

        return res