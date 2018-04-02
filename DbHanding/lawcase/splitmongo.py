import pymongo, logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='test.log',
                filemode='w')

if __name__ == '__main__':
    con = pymongo.MongoClient("192.168.68.11", 20000)
    col = con.divorceCase3.searchPerform
    col1 = con.divorceCase3.searchResTfidf
    col2 = con.divorceCase3.searchResWeightTfidf
    col3 = con.divorceCase3.searchResLdaVec
    col4 = con.divorceCase3.searchResDoc2vec

    cur = col.find(no_cursor_timeout = True)
    for item in cur:
        newItem = {}
        newItem['searchId'] = item['searchId']
        newItem['ref'] = item['ref']
        newItem['tag'] = item['tag']
        newItem['res'] = item['resByKeyWord']
        col1.insert(newItem)
        newItem['res'] = item['resByTfidf']
        col2.insert(newItem)
        newItem['res'] = item['resByLda']
        col3.insert(newItem)
        newItem['res'] = item['resByTest']
        col4.insert(newItem)
    cur.close()
    logging.info("finish")