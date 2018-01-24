from .collections import searchPerform

class statutePerform():
    def __init__(self, sp):
        self.ref = sp.getStatuteSetList('ref')
        self.top10refByKeywordList = sp.getStatuteSetList('resByKeyWord', 10)
        self.top20refByKeywordList = sp.getStatuteSetList('resByKeyWord', 20)
        self.top50refByKeywordList = sp.getStatuteSetList('resByKeyWord', 50)
        self.top10refByTfidfList = sp.getStatuteSetList('resByTfidf', 10)
        self.top20refByTfidfList = sp.getStatuteSetList('resByTfidf', 20)
        self.top50refByTfidfList = sp.getStatuteSetList('resByTfidf', 50)
        self.top10refByLdaList = sp.getStatuteSetList('resByLda', 10)
        self.top20refByLdaList = sp.getStatuteSetList('resByLda', 20)
        self.top50refByLdaList = sp.getStatuteSetList('resByLda', 50)

    def getcoverCount(self, refset1, refset2):
        #refset1为标准法条引用集合
        #refset2为搜索结果的法条引用集合
        count = 0
        for ref in refset1:
            if ref in refset2:
                count += 1
        return count

    def getPrecisionAndRecall(self, refset1, refset2, option):
        # refsetlist1为标准法条引用集合
        # refsetlist2为搜索结果的法条引用集合

        coverCount = self.getcoverCount(refset1, refset2)

        if option == 0: #返回precision
            if len(refset2) != 0:
                res = round(coverCount / len(refset2), 3)
            else:
                res = 0
        elif option == 1:  # 返回recall
            if len(refset1) != 0:
                res = round(coverCount / len(refset1), 3)
            else:
                res = 0
        elif option == 2:  # 返回[p,r]
            if len(refset2) != 0:
                precision = round(coverCount / len(refset2), 3)
            else:
                precision = 0
            if len(refset1) != 0:
                recall = round(coverCount / len(refset1), 3)
            else:
                recall = 0
            res = [recall, precision]
        else:
            return None

        return res

    def formatRate(self, rate, option):
        if option == 0 or option == 1:
            res = [0 for i in range(10)]
            for p in rate:
                if p == 0:
                    res[0] += 1
                else:
                    res[int((p-0.00001)*10)%10] += 1
        else:
            res = rate

        return res

    def getmeanPRF(self, ratelist):
        P = 0
        R = 0
        F1 = 0
        num = 0

        for rate in ratelist:
            P += rate[1]
            R += rate[0]
            F1 += 2 * rate[0] * rate[1] / (rate[0] + rate[1]) if rate[0] + rate[1] !=0 else 0
            num += 1

        return round(P / num, 3), round(R / num, 3), round(F1 / num, 3)

    def getStatutePerform(self, option):
        res = dict()

        k10List = []
        k20List = []
        k50List = []
        t10List = []
        t20List = []
        t50List = []
        l10List = []
        l20List = []
        l50List = []

        for r, rk10, rk20, rk50, rk10, rt20, rt50, rl10, rl20, rl50 in \
                zip(self.ref, self.top10refByKeywordList, self.top20refByKeywordList, self.top50refByKeywordList,\
                    self.top10refByTfidfList, self.top20refByTfidfList, self.top50refByTfidfList,\
                    self.top10refByLdaList, self.top20refByLdaList, self.top50refByLdaList):

            k10List.append(self.getPrecisionAndRecall(r, rk10, option))
            k20List.append(self.getPrecisionAndRecall(r, rk20, option))
            k50List.append(self.getPrecisionAndRecall(r, rk50, option))
            t10List.append(self.getPrecisionAndRecall(r, rk10, option))
            t20List.append(self.getPrecisionAndRecall(r, rt20, option))
            t50List.append(self.getPrecisionAndRecall(r, rt50, option))
            l10List.append(self.getPrecisionAndRecall(r, rl10, option))
            l20List.append(self.getPrecisionAndRecall(r, rl20, option))
            l50List.append(self.getPrecisionAndRecall(r, rl50, option))

        if option == 0 or option == 1:
            res['t10k'] = self.formatRate(k10List, option)
            res['t20k'] = self.formatRate(k20List, option)
            res['t50k'] = self.formatRate(k50List, option)
            res['t10t'] = self.formatRate(t10List, option)
            res['t20t'] = self.formatRate(t20List, option)
            res['t50t'] = self.formatRate(t50List, option)
            res['t10l'] = self.formatRate(l10List, option)
            res['t20l'] = self.formatRate(l20List, option)
            res['t50l'] = self.formatRate(l50List, option)
        else:
            precision = [0 for i in range(9)]
            recall = [0 for i in range(9)]
            f1 = [0 for i in range(9)]
            precision[0], recall[0], f1[0] = self.getmeanPRF(k10List)
            precision[1], recall[1], f1[1] = self.getmeanPRF(k20List)
            precision[2], recall[2], f1[2] = self.getmeanPRF(k50List)
            precision[3], recall[3], f1[3] = self.getmeanPRF(t10List)
            precision[4], recall[4], f1[4] = self.getmeanPRF(t20List)
            precision[5], recall[5], f1[5] = self.getmeanPRF(t50List)
            precision[6], recall[6], f1[6] = self.getmeanPRF(l10List)
            precision[7], recall[7], f1[7] = self.getmeanPRF(l20List)
            precision[8], recall[8], f1[8] = self.getmeanPRF(l50List)

            res['precision'] = precision
            res['recall'] = recall
            res['f1'] = f1

        return res