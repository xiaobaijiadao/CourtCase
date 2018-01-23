from .collections import searchPerform

class casePerform():
    def __init__(self, sp):
        self.referenceNum = sp.getReferenceNum()
        self.rnAndCc = sp.getReferenceNumAndCoverCount()

    def computePrecision(self, tag):
        # tag为长度为50的标记list,记录搜索结果是否合格
        truecount = 0
        allCount = 0
        for t in tag:
            truecount += t
            allCount += 1
        return round(float(truecount / allCount), 3)

    def getPrecision(self, rn, rlist, clist):
        # rn为500条测试集中的某一条案件的法条个数
        # rlist为搜索到的前五十条中各条案件的法条个数的list
        # clist为搜索到的前五十条中各条案件的法条覆盖rn的个数的list
        tag = []  # 标记案件是否为合格结果
        for r, c in zip(rlist, clist):
            if rn == 0 or r == 0:
                tag.append(0)
                continue

            if float(c) / float(rn) + float(c) / float(r) >= 1:
                tag.append(1)
            else:
                tag.append(0)

        top10Precision = self.computePrecision(tag[:10])
        top20Precision = self.computePrecision(tag[:20])
        top50Precision = self.computePrecision(tag[:50])

        return top10Precision, top20Precision, top50Precision

    def formatPrecision(self, precisionlist):
        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for p in precisionlist:
            if p == 1.0:
                res[9] += 1
            else:
                res[int(p * 10)%10] += 1
        return res

    def getCasePerform(self):
        res = dict()
        top10PrecisionByKeywordList = []
        top20PrecisionByKeywordList = []
        top50PrecisionByKeywordList = []
        top10PrecisionByTfidfList = []
        top20PrecisionByTfidfList = []
        top50PrecisionByTfidfList = []
        top10PrecisionByLdaList = []
        top20PrecisionByLdaList = []
        top50PrecisionByLdaList = []

        for rn, rk, rt, rl, ck, ct, cl in \
                zip(self.referenceNum, self.rnAndCc['ReferenceNumByKeyword'], self.rnAndCc['ReferenceNumByTfidf'],
                    self.rnAndCc['ReferenceNumByLda'], self.rnAndCc['CoverCountByKeyword'], self.rnAndCc['CoverCountByTfidf'],
                    self.rnAndCc['CoverCountByLda']):
            p10k, p20k, p50k = self.getPrecision(rn, rk, ck)
            p10t, p20t, p50t = self.getPrecision(rn, rt, ct)
            p10l, p20l, p50l = self.getPrecision(rn, rl, cl)

            top10PrecisionByKeywordList.append(p10k)
            top20PrecisionByKeywordList.append(p20k)
            top50PrecisionByKeywordList.append(p20k)

            top10PrecisionByTfidfList.append(p10t)
            top20PrecisionByTfidfList.append(p20t)
            top50PrecisionByTfidfList.append(p50t)

            top10PrecisionByLdaList.append(p10l)
            top20PrecisionByLdaList.append(p20l)
            top50PrecisionByLdaList.append(p50l)

        res['t10k'] = self.formatPrecision(top10PrecisionByKeywordList)
        res['t20k'] = self.formatPrecision(top20PrecisionByKeywordList)
        res['t50k'] = self.formatPrecision(top50PrecisionByKeywordList)
        res['t10t'] = self.formatPrecision(top10PrecisionByTfidfList)
        res['t20t'] = self.formatPrecision(top20PrecisionByTfidfList)
        res['t50t'] = self.formatPrecision(top50PrecisionByTfidfList)
        res['t10l'] = self.formatPrecision(top10PrecisionByLdaList)
        res['t20l'] = self.formatPrecision(top20PrecisionByLdaList)
        res['t50l'] = self.formatPrecision(top50PrecisionByLdaList)

        return res