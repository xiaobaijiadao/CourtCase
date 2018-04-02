# from gensim import corpora, models
# import pymongo
#
# tactics = ['resByKeyWord', 'resByTfidf', 'resByLda', 'resByTest']
#
# def getStatuteSetList(option, limit=50):
#     # 获取不同方法得到的50条数据中前10条，前20条和前50条的法条集合
#     statuteSetList = []
#     con = pymongo.MongoClient('192.168.68.11', 20000)
#     col1 = con.divorceCase3.searchPerform
#
#
#     cur = col1.find_one(no_cursor_timeout=True)
#
#     if option == 'ref':
#         for item in cur:
#             statutes = set(item['ref'])
#             statuteSetList.append(statutes)
#     elif option in tactics:
#         item = cur
#         statutes = []
#         List = item[option]
#         sortList = None
#
#         k1 = 'sim1'
#         k2 = 'sim2'
#         sortList1 = sorted(List, key=lambda item: item[k1], reverse=True)
#         sortList2 = sorted(List, key=lambda item: item[k2], reverse=True)
#
#         for l1, l2 in zip(sortList1, sortList2):
#             print(l1)
#             print(l2)
#             print()
#
#         for i in sortList1[:limit]:
#             statutes.extend(i['ref'])
#
#         statuteSetList.append(set(statutes))
#
#     return statuteSetList
#
# if __name__ == '__main__':
#      #getStatuteSetList(tactics[0])
#      a = [(6,0),(3, 1),(2,7),(10,5),(9,7),(6,0)]
#      print(sorted(a,key=lambda  item: item[1]))


if __name__ == '__main__':
    import time
    print("start")
    s1 = time.time()
    time.sleep(3)
    s2 = time.time()
    print(s2-s1)