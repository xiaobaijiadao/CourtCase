# coding:utf-8

# version1
# 输入：id,[key->tfidf]...
# 索引表 key,[id->tfidf]...

# version2
# 索引表 key->[(id,times),]->[pos,]
# eg:    key->[(1,2)(4,1)]->[2,7,1]

import pymongo, re

if __name__ == '__main__':
    # 连接数据库
    con = pymongo.MongoClient()
    col1 = con.Lawcase.tf_idf
    col2 = con.Lawcase.indexTable

    indexDict = dict()

    stopwords = {}.fromkeys([line.rstrip() for line in open('stopWords.txt')])
    print(stopwords)

    for item in col1.find():
        for k,v in item.items():
            print(k,v)
            if k == "wordslist":
                for wt in v:    #v -> [{"word": , "tfidf": },...]
                    if wt["word"] not in stopwords and re.search(r'[0-9a-zA-Z ]+', wt["word"]) == None:
                        if wt["word"] in indexDict:
                            indexDict[wt["word"]]["caselist"].append({"caseid":item["lawcaseid"], "tfidf":wt["tfidf"]})
                        else:
                            dic = dict()
                            dic["key"] = wt["word"]
                            caselist = list()
                            caselist.append({"caseid":item["lawcaseid"], "tfidf":wt["tfidf"]})
                            dic["caselist"] = caselist
                            indexDict[wt["word"]] = dic

    for k,v in indexDict.items():
        print(v)
        col2.insert(v)