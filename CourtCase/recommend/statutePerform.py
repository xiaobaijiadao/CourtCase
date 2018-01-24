from .collections import searchPerform, searchEvaluate

class statutePerform():
    tactics = ['k10', 'k20', 'k50', 't10', 't20', 't50', 'l10', 'l20', 'l50']

    def __init__(self, sp):
        self.sp = sp

    def getDataFromDB(self):
        self.ref = self.sp.getStatuteSetList('ref')
        self.top10refByKeywordList = self.sp.getStatuteSetList('resByKeyWord', 10)
        self.top20refByKeywordList = self.sp.getStatuteSetList('resByKeyWord', 20)
        self.top50refByKeywordList = self.sp.getStatuteSetList('resByKeyWord', 50)
        self.top10refByTfidfList = self.sp.getStatuteSetList('resByTfidf', 10)
        self.top20refByTfidfList = self.sp.getStatuteSetList('resByTfidf', 20)
        self.top50refByTfidfList = self.sp.getStatuteSetList('resByTfidf', 50)
        self.top10refByLdaList = self.sp.getStatuteSetList('resByLda', 10)
        self.top20refByLdaList = self.sp.getStatuteSetList('resByLda', 20)
        self.top50refByLdaList = self.sp.getStatuteSetList('resByLda', 50)

    def getcoverCount(self, refset1, refset2):
        #refset1为标准法条引用集合
        #refset2为搜索结果的法条引用集合
        count = 0
        for ref in refset1:
            if ref in refset2:
                count += 1
        return count

    def getPrecisionAndRecallAndF1(self, refset1, refset2):
        # refsetlist1为标准法条引用集合
        # refsetlist2为搜索结果的法条引用集合

        coverCount = self.getcoverCount(refset1, refset2)

        if len(refset2) != 0:
            precision = round(coverCount / len(refset2), 3)
        else:
            precision = 0
        if len(refset1) != 0:
            recall = round(coverCount / len(refset1), 3)
        else:
            recall = 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall !=0 else 0
        res = (recall, precision, f1)

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

    def genEvaluate(self):
        result = {
            'precision' : [
                {
                    'tacticsName' : i,
                    'value' : [],
                    'meanValue' : 0,
                } for i in statutePerform.tactics
            ],
            'recall': [
                {
                    'tacticsName': i,
                    'value': [],
                    'meanValue': 0,
                } for i in statutePerform.tactics
            ],
            'f1': [
                {
                    'tacticsName': i,
                    'value': [],
                    'meanValue': 0,
                } for i in statutePerform.tactics
            ],

        }

        self.getDataFromDB()

        for r, k10, k20, k50, t10, t20, t50, l10, l20, l50 in \
                zip(self.ref, self.top10refByKeywordList, self.top20refByKeywordList, self.top50refByKeywordList,\
                    self.top10refByTfidfList, self.top20refByTfidfList, self.top50refByTfidfList,\
                    self.top10refByLdaList, self.top20refByLdaList, self.top50refByLdaList):

            k10p, k10r, k10f = self.getPrecisionAndRecallAndF1(r, k10)
            result['precision'][0]['value'].append(k10p)
            result['recall'][0]['value'].append(k10r)
            result['f1'][0]['value'].append(k10f)

            k20p, k20r, k20f = self.getPrecisionAndRecallAndF1(r, k20)
            result['precision'][1]['value'].append(k20p)
            result['recall'][1]['value'].append(k20r)
            result['f1'][1]['value'].append(k20f)

            k50p, k50r, k50f = self.getPrecisionAndRecallAndF1(r, k50)
            result['precision'][2]['value'].append(k50p)
            result['recall'][2]['value'].append(k50r)
            result['f1'][2]['value'].append(k50f)

            t10p, t10r, t10f = self.getPrecisionAndRecallAndF1(r, t10)
            result['precision'][3]['value'].append(t10p)
            result['recall'][3]['value'].append(t10r)
            result['f1'][3]['value'].append(t10f)

            t20p, t20r, t20f = self.getPrecisionAndRecallAndF1(r, t20)
            result['precision'][4]['value'].append(t20p)
            result['recall'][4]['value'].append(t20r)
            result['f1'][4]['value'].append(t20f)

            t50p, t50r, t50f = self.getPrecisionAndRecallAndF1(r, t50)
            result['precision'][5]['value'].append(t50p)
            result['recall'][5]['value'].append(t50r)
            result['f1'][5]['value'].append(t50f)

            l10p, l10r, l10f = self.getPrecisionAndRecallAndF1(r, l10)
            result['precision'][6]['value'].append(l10p)
            result['recall'][6]['value'].append(l10r)
            result['f1'][6]['value'].append(l10f)

            l20p, l20r, l20f = self.getPrecisionAndRecallAndF1(r, l20)
            result['precision'][7]['value'].append(l20p)
            result['recall'][7]['value'].append(l20r)
            result['f1'][7]['value'].append(l20f)

            l50p, l50r, l50f = self.getPrecisionAndRecallAndF1(r, l50)
            result['precision'][8]['value'].append(l50p)
            result['recall'][8]['value'].append(l50r)
            result['f1'][8]['value'].append(l50f)

        for value in result.values():
            for item in value:
                item['meanValue'] = round(sum(item['value'])/len(item['value']), 3)

        return result

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

    def getStatutePerform(self, option):
        res = dict()

        if option == 0 or option == 1:
            data = None
            if option == 0:
                data = searchEvaluate().getRateByName('statutePrecison')
            else:
                data = searchEvaluate().getRateByName('statuteRecall')

            res['t10k'] = self.formatRate(data[0], option)
            res['t20k'] = self.formatRate(data[1], option)
            res['t50k'] = self.formatRate(data[2], option)
            res['t10t'] = self.formatRate(data[3], option)
            res['t20t'] = self.formatRate(data[4], option)
            res['t50t'] = self.formatRate(data[5], option)
            res['t10l'] = self.formatRate(data[6], option)
            res['t20l'] = self.formatRate(data[7], option)
            res['t50l'] = self.formatRate(data[8], option)

        else:
            se = searchEvaluate()
            res['precision'] = se.getMeanRateByName('statutePrecison')
            res['recall'] = se.getMeanRateByName('statuteRecall')
            res['f1'] = se.getMeanRateByName('statuteF1')

        return res