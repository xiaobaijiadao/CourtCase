# coding:utf-8

# version1
# 输入：id,[key->tfidf]...
# 索引表 key,[id->tfidf]...

# version2
# 索引表 key->[(id,times),]->[pos,]
# eg:    key->[(1,2)(4,1)]->[2,7,1]

import pymongo

if __name__ == '__main__':
    # 连接数据库
    con = pymongo.MongoClient()
    col1 = con.caseTest.allCaseTfIdf
    col2 = con.caseTest.indexTable

    indexDict = dict()

    for item in col1.find():
        for k, v in item.items():
            if k != "id" and k != "_id":
                print(k,v)
                print("enter")
                if k in indexDict:
                    indexDict[k][str(item["id"])] = v
                else:
                    dic = dict()
                    dic["key"] = k
                    dic[str(item["id"])] = v
                    indexDict[k] = dic
            print(indexDict)

    for k,v in indexDict.items():
        print(v)
        col2.insert(v)