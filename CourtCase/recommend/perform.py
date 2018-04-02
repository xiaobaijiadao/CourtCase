from .collections import searchEvaluate, searchResEvaluate

class searchEvaluateDispaly():

    def __init__(self):
        self.tactics = ['key', 'tfidf', 'lda', 'test']
        self.limit = [1, 3, 5, 10, 20, 50]
        self.gentacticsCP()

    def gentacticsCP(self):
        self.tacticsCP = []
        for tactic in self.tactics:
            for l in self.limit:
                self.tacticsCP.append(tactic + str(l))

    def formatRate(self, rate, option):
        if option == 0 or option == 1:
            res = [0 for i in range(10)]
            for p in rate:
                if p <= 0.1:
                    res[0] += 1
                elif p <= 0.2:
                    res[1] += 1
                elif p <= 0.3:
                    res[2] += 1
                elif p <= 0.4:
                    res[3] += 1
                elif p <= 0.5:
                    res[4] += 1
                elif p <= 0.6:
                    res[5] += 1
                elif p <= 0.7:
                    res[6] += 1
                elif p <= 0.8:
                    res[7] += 1
                elif p <= 0.9:
                    res[8] += 1
                else:
                    res[9] += 1
            for r in res:
                r = round(r/len(rate), 3)*100
        else:
            res = rate

        return res

    def getStatutePerform(self, option, prf = 'p', tag = '2'):
        res = dict()

        if option == 0 or option == 1:
            data = None
            if option == 0:
                data = searchEvaluate().getRateByName('statutePrecison', tag)
            else:
                data = searchEvaluate().getRateByName('statuteRecall', tag)

            for i in range(len(self.tacticsCP)):
                res[self.tacticsCP[i]] = self.formatRate((data[i], option))

        else:
            result = {
                'lineTag' : ['nosort_1','presort_1','nosort_2','presort_2'],
                'x' : [],
                'v' : [],
                'loop' : 0,
            }
            x1 = []
            x2 = []
            v1 = []
            v2 = []
            r = list()
            se = searchEvaluate()
            key = 'Precision'
            if prf == 'p':
                key = key
            elif prf == 'r':
                key = 'Recall'
            elif prf == 'f':
                key = 'F1'
            else:
                print('key error!')
                return None

            for i in range(2):
                r.append(se.getMeanRateByName('statutes'+str(i)+key, tag))
            for i in range(2):
                r.append(se.getAllRateByName('statutes'+str(i)+key, tag))

            y = len(self.limit)
            for i in range(1,len(self.tacticsCP)+1):
                if i % y >= 1 and i % y <= 3:
                    x1.append(self.tacticsCP[i - 1])
                else:
                    x2.append(self.tacticsCP[i - 1])

            for value in r:
                l1 = []
                l2 = []
                for i in range(1,len(self.tacticsCP)+1):
                    if i%y >= 1 and i%y <= 3:
                        l1.append(value[i - 1])
                    else:
                        l2.append(value[i - 1])
                v1.append(l1)
                v2.append(l2)

            result['x'].append(x1)
            result['x'].append(x2)
            result['v'].append(v1)
            result['v'].append(v2)
            result['loop'] = 2
            res = result

        return res


class searchStatuteEvaluateDisplay():

    def __init__(self):
        pass

    def getStatutePerform(self, tag, limit):
        res = searchResEvaluate().getPrecisionAndName(tag, limit)
        return res