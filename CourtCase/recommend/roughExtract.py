# 第一次：粗提取。
# 获取输入，进行分词，从索引表中提取出存在分词的案件的id
# 输入：从前端获取的字符串
# 输出：按tfidf值排序的id列表

import jieba
from .docs import Dao


class roughExtract:
    def __init__(self, input):
        self.input = input

    def token(self):#分词
        return jieba.cut_for_search(self.input)

    def getIndexList(self):#获取第一次提取列表
        db = Dao()
        db.getCollection('caseTest', 'indexTable')

        result = dict()
        print(self.input)
        seg = self.token()
        for s in seg:
            for res in db.findByKey('key', s):
                for k,v in res.items():
                    if k != '_id' and k != 'key':
                        result[k] = result[k]+v if k in result else v

        return sorted(result.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    r = roughExtract("索要离婚赔偿100000元")
    print(r.getIndexList())