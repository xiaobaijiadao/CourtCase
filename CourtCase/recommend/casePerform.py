from .collections import searchEvaluate

class casePerform():
    tactics = ['k10', 'k20', 'k50', 't10', 't20', 't50', 'l10', 'l20', 'l50']

    def __init__(self, sp):
        self.sp = sp

    def getDataFromDB(self):
        self.referenceNum = self.sp.getReferenceNum()
        self.rnAndCc = self.sp.getReferenceNumAndCoverCount()

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

    def genEvaluate(self):
        result = {
            'precision' : [
                {
                    'tacticsName' : i,
                    'value' : [],
                    'meanValue' : 0,
                } for i in casePerform.tactics
            ],
        }

        self.getDataFromDB()
        for rn, rk, rt, rl, ck, ct, cl in \
                zip(self.referenceNum, self.rnAndCc['ReferenceNumByKeyword'], self.rnAndCc['ReferenceNumByTfidf'],
                    self.rnAndCc['ReferenceNumByLda'], self.rnAndCc['CoverCountByKeyword'],
                    self.rnAndCc['CoverCountByTfidf'],
                    self.rnAndCc['CoverCountByLda']):
            k10p, k20p, k50p = self.getPrecision(rn, rk, ck)
            t10p, t20p, t50p = self.getPrecision(rn, rt, ct)
            l10p, l20p, l50p = self.getPrecision(rn, rl, cl)

            result['precision'][0]['value'].append(k10p)
            result['precision'][1]['value'].append(k20p)
            result['precision'][2]['value'].append(k50p)
            result['precision'][3]['value'].append(t10p)
            result['precision'][4]['value'].append(t20p)
            result['precision'][5]['value'].append(t50p)
            result['precision'][6]['value'].append(l10p)
            result['precision'][7]['value'].append(l20p)
            result['precision'][8]['value'].append(l50p)

        for value in result.values():
            for item in value:
                item['meanValue'] = round(sum(item['value'])/len(item['value']), 3)

        return result

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

        data = searchEvaluate().getRateByName('casePrecision')

        res['t10k'] = self.formatPrecision(data[0])
        res['t20k'] = self.formatPrecision(data[1])
        res['t50k'] = self.formatPrecision(data[2])
        res['t10t'] = self.formatPrecision(data[3])
        res['t20t'] = self.formatPrecision(data[4])
        res['t50t'] = self.formatPrecision(data[5])
        res['t10l'] = self.formatPrecision(data[6])
        res['t20l'] = self.formatPrecision(data[7])
        res['t50l'] = self.formatPrecision(data[8])

        return res

