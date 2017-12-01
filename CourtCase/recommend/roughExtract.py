# 第一次：粗提取。
# 获取输入，进行分词，从索引表中提取出存在分词的案件的id
# 输入：从前端获取的字符串
# 输出：按tfidf值排序的id列表

import jieba
from .collections import indexTable


class roughExtract:
    def __init__(self, input):
        self.input = input

    def token(self):#分词
        return jieba.cut_for_search(self.input)

    def getIndexList(self):#获取第一次提取列表
        indextb = indexTable()

        midResult1 = dict()
        # print(self.input)

        #所有包含关键字的案件的tfidf求和值和包含关键字总数
        seg = self.token()
        for s in seg:
            for k,v in indextb.getCaselistByKey(s).items():
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
        #在同一个wordsCount下按dfidf排序
        for k,v in midResult2.items():
            midResult2[k] = sorted(v, key=lambda item: item[1],  reverse=True)

        #对wordsCount排序
        midResult3 = sorted(midResult2.items(), key=lambda item: item[0],  reverse=True)
        res = list()
        for item in midResult3:
            for i in item[1]:
                res.append(i[0])
                if len(res)>50:
                    break
        print(res)
        print(len(res))

        return res


if __name__ == '__main__':
    r = roughExtract("索要离婚赔偿100000元")
    res = r.getIndexList()
    print(len(res))
    print(res)

