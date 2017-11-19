#对第二次处理后得到的搜索结果的所有案件按某种方法进行打分，获取最终展示列表
#输入：第二次处理列表
#输出：最终结果列表



class point:
    #weight[案由案件基本情况相似度，法院层级码，结案年月日]

    def __init__(self, similarities):
        self.similarities = similarities

    def pointCase(self):
        self.similarities = sorted(self.similarities, key=lambda x:x[1], reverse=True)

    def getRes(self):
        return self.similarities
