#第二次：进一步缩小范围，考虑多方面相似度
#输入：前端获取的字符串，粗提取得到的列表
#输出：进一步缩小范围的搜索结果的列表

from .docs import Dao
import jieba.analyse
from gensim import corpora, models, similarities

class fineExtract:

    def __init__(self, input, roughRes):
        self.input = input
        self.roughRes = roughRes

    #获取案件的原告诉称、被告辩称和查明事实段信息，按类存入dict
    def getRoughCaseInf(self):
        db = Dao()
        db.getCollection('caseTest', 'indexTable')

        caseMultidimInfo = dict()
        wzay = list()
        ygscd = list()
        bgbcd = list()
        cmssd = list()

        i = 0
        for case in self.roughRes:
            cs = db.findByKey(id, case[0])[0]
            for k,v in cs.items():
                if k == "YGSCD":
                    ygscd.append(v)
                elif k == "BGBCD":
                    bgbcd.append(v)
                elif k == "CMSSD":
                    cmssd.append(v)
                elif k == "WZAY":
                    wzay.append(v)

            i += 1
            if i > 100:
                break

        caseMultidimInfo['ygscd'] = ygscd
        caseMultidimInfo['bgbcd'] = bgbcd
        caseMultidimInfo['cmssd'] = cmssd
        caseMultidimInfo['wzay'] = wzay

        return caseMultidimInfo

    #返回查询信息分别与每个案件的原告诉称、被告辩称和查明事实段信息的文档相似度
    def computeEachSimilarity(self, caseInfoList):
        #获取所有案件包括输入信息的分词列表组成的列表
        texts = list()
        for caseInfo in caseInfoList:
            text = list()
            for x in jieba.cut(caseInfo, cut_all=False):
                text.append(x)
            texts.append(text)
        print(texts)
        #获取词袋
        dictionary = corpora.Dictionary(texts)
        #将每条文档转换为向量
        corpus = [dictionary.doc2bow(text) for text in texts]
        #计算tfidf模型
        tfidf = models.TfidfModel(corpus)
        #获取每个文段的基于该tfidf模型的向量
        corpus_tfidf = tfidf[corpus]
        #建立LSI模型
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
        #将文档映射到该低维空间，个人理解就是降维
        corpus_lsi = lsi[corpus_tfidf]

        #建立用于查找输入信息与已有文档相似度的索引
        index= similarities.MatrixSimilarity(corpus_lsi)

        #将输入查询信息向量化

        inputToken = list()
        for x in jieba.cut(self.input, cut_all=False):
            inputToken.append(x)
        print(inputToken)
        query_bow = dictionary.doc2bow(inputToken)
        #利用之前建好的tfidf和lsi模型将其映射到该低维空间
        query_tfidf = tfidf[query_bow]
        query_lsi = lsi[query_tfidf]

        sim = index[query_lsi]

        return sorted(enumerate(sim), key=lambda item: item[0])

    #
    def collectSimilarity(self):
        caseMultidimInfo = self.getRoughCaseInf()

        ygscSimilarity = self.computeEachSimilarity(caseMultidimInfo['ygscd'])
        bgbcdSimilarity = self.computeEachSimilarity(caseMultidimInfo['bgbcd'])
        cmssdSimilarity = self.computeEachSimilarity(caseMultidimInfo['cmssd'])
        wzaySimilarity = self.computeEachSimilarity(caseMultidimInfo['wzay'])

        similarity = list()
        for i in range(len(ygscSimilarity)):
            similarity.append((self.roughRes[i][0], ygscSimilarity[i][1]+bgbcdSimilarity[i][1]+cmssdSimilarity[i][1]+wzaySimilarity[i][1]))

        return similarity

    def getResult(self):
        res = self.collectSimilarity()
        return res


if __name__ == '__main__':
    input = "由于夫妻关系经济纠纷家庭发生争执"
    roughRes = [
        u"原告秦大宽诉称：2014年12月19日13时许，被告文春花驾驶渝HL1777普通小型客车在普子镇中心卫生院门前路段倒车时与原告秦大宽相撞，造成原告秦大宽受伤的交通事故。原告秦大宽受伤后，被告文春花在普子场上一家药店为其购买了一些药品，12月20日，原告秦大宽到普子中心卫生院摄片检查：左桡骨远程横断骨折，并行石膏外固定术，每半月复查一次。2015年1月6日，原告秦大宽到彭水中医院复查，诊断为左桡骨远程骨折，左尺骨呈撕脱性骨折，继续外固定半月，当日返回普子，入住普子卫生院就近住院治疗3天出院。院外复查用药至2015年3月30日，其伤残程度经司法鉴定为十级伤残。综上，原告秦大宽的伤经彭水县公安局交警大队查明，是被告文春花于2014年12月19日13时许，在彭水县普子镇卫生院门前路段倒车时撞伤所致，文春花应当承担本案的全部事故责任，故该事故车辆投保于被告中华联合财产保险股份有限公司重庆分公司彭水支公司，有效期至2015年7月14日止。故原告为维护其合法权利，诉至法院要求判令：一、被告中华联合财产保险股份有限公司重庆分公司彭水支公司在机动车交通事故责任强制保险赔偿限额内赔偿原告秦大宽医药费2478．7元、误工费7140元、护理费210元、住院伙食补助费90元、残疾赔偿金18031元、鉴定费700元、交通费1221元、精神损害抚慰金4000元，以上合计33870．7元，不足部分由被告中华联合财产保险股份有限公司重庆分公司彭水支公司在第三者商业保险赔偿限额内赔偿，仍有不足的由被告文春花赔偿；二、本案案件受理费由被告中华联合财产保险股份有限公司重庆分公司彭水支公司、文春花负担。",
        u"原告徐某诉称：原、被告于2011年10月通过网络相识，于××××年××月××日登记结婚，至今未生育。双方婚后初期感情一般。自2015年初开始，双方在性格脾气上的不合逐渐显露，经常为家庭琐事及经济问题发生争执，且被告对原告极不关心，致使夫妻感情出现隔阂。原告于2015年8月起回娘家居住，双方开始分居。现原告认为夫妻感情已经破裂，故起诉要求准予原、被告离婚。",
        u"原告冯和龙诉称，被告戴建华、常芳夫妇于2015年2月21日以需支付人员工资、吊车加油为由向原告借款100000元，并承诺等外面工程款到手后即偿还原告。后两被告未还款，请求判令被告偿还原告借款100000元及利息25000元。"
    ]
    fine = fineExtract(input, roughRes)
    print(fine.computeEachSimilarity(roughRes))