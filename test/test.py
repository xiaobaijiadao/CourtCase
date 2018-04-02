from test import roughExtract as trx
import pymongo, logging
from gensim import models, corpora
import time

CON = pymongo.MongoClient('192.168.68.11', 20000)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='test.log',
                filemode='w')

def getcoverCount(standardList, testList):
    count = len(set(standardList) & set(testList))
    return count

def getMethod3FromTxt(option):
    res = []
    path = None
    if option == '2':
        path = "txt/testTop50.txt"
    elif option == '3':
        path = "txt/testTop50.txt"
    else:
        path = "txt/testTop50.txt"

    with open(path) as fp:
        for line in fp.readlines():
            l = line.split('\t')
            standard = l[0]
            search = l[1].split(' ')
            if '\n' in search:
                search.remove('\n')
            res.append((standard, search))
    return res

def gettestresult(searchRes, option, col, referenceStandard):
    idlist = searchRes
    # if option != "doc":
    #     idlist = [r['id'] for r in list_format(searchRes, option)]

    result = []
    for id in idlist:
        case = dict()
        case['id'] = id
        reference = [ref['name'].strip() + ref['levelone'].strip() \
                     for ref in col.find_one({"fullTextId": id})['references']]
        case['ref'] = reference
        case['covercount'] = getcoverCount(referenceStandard, reference)
        case['sim1'] = round(case['covercount']/(len(referenceStandard)+len(case['ref'])-case['covercount']), 4)
        P = case['covercount']/len(case['ref'])
        R = case['covercount']/len(referenceStandard)
        case['sim2'] = round(2 * P * R / (P + R), 4) if (P+R) != 0 else 0
        result.append(case)
    return result

def test(tag, option):
    #tag: 2:验证集，3测试集
    #option： 1.tfidf 2.weightedTfidf 3.lda(vec上下浮动)
    #        4.lda(dis，direct浮动)  5.lda（最大topic浮动）6.lda(遍历所有) 7.doc2vec
    if tag not in ['2', '3', '4']:
        raise("tag error!")
    if option not in ['1', '2', '3', '4', '5', '6', '7']:
        raise("option error!")

    col1 = CON.divorceCase3.alldata
    col2 = CON.divorceCase3.lawreference
    col3 = None
    if option == '1':
        col3 = CON.divorceCase3.searchResTfidf
    elif option == '2':
        col3 = CON.divorceCase3.searchResWeightTfidf
    elif option == '3':
        col3 = CON.divorceCase3.searchResLdaVec
    elif option == '4':
        col3 = CON.divorceCase3.searchResLdaDisDirect
    elif option == '5':
        col3 = CON.divorceCase3.searchResLdaTopic
    elif option == '6':
        col3 = CON.divorceCase3.searchResLdaAll
    else:
        col3 = CON.divorceCase3.searchResDoc2vec
        i = 1
        for caseids in getMethod3FromTxt(tag):
            if col3.find_one({"searchId": caseids[0]}) is not None:
                continue
            case = col1.find_one({"fullTextId": caseids[0]})
            referenceStandard = [ref['name'].strip() + ref['levelone'].strip() \
                                 for ref in col2.find_one({"fullTextId": case['fullTextId']})['references']]

            res = dict()
            res['searchId'] = case['fullTextId']
            res['ref'] = referenceStandard
            res['tag'] = case['tag']

            res['resByTest'] = gettestresult(caseids[1], "doc", col2, referenceStandard)

            col3.insert(res)
            logging.info("第 %d 次写入" % i)
            i += 1
        logging.info('finish!')
        return None

    i = 1
    cur = col1.find({"tag": tag}, no_cursor_timeout=True)
    for caseids in cur:
        searchId = caseids['fullTextId']
        if col3.find_one({"searchId": searchId}) is not None:
            continue
        case = col1.find_one({"fullTextId": searchId})
        referenceStandard = [ref['name'].strip() + ref['levelone'].strip() \
                             for ref in col2.find_one({"fullTextId": case['fullTextId']})['references']]

        res = dict()
        res['searchId'] = case['fullTextId']
        res['ref'] = referenceStandard
        res['tag'] = case['tag']

        query = case['plaintiffAlleges']['text'] \
                + case['defendantArgued']['text'] \
                + case['factFound']['text']
        rough = trx.roughExtract(query, CON)

        if option == '1':
            roughRes = rough.getIndexListbyTfidf()
            res['res'] = gettestresult(roughRes, "tfidf", col2, referenceStandard)
        elif option == '2':
            roughRes = rough.getIndexListbyWeightTfidf()
            res['res'] = gettestresult(roughRes, "weighttfidf", col2, referenceStandard)
        elif option == '3':
            lda_model = models.LdaModel.load('divorce3/lda.model')
            text2vec = corpora.Dictionary.load('divorce3/lda.dct')
            roughRes = rough.getIndexListbyLda(1, lda_model, text2vec)
            res['res'] = gettestresult(roughRes, "lda", col2, referenceStandard)
        elif option == '4':
            lda_model = models.LdaModel.load('divorce3/lda.model')
            text2vec = corpora.Dictionary.load('divorce3/lda.dct')
            roughRes = rough.getIndexListbyLda(2, lda_model, text2vec)
            res['res'] = gettestresult(roughRes, "lda", col2, referenceStandard)
        elif option == '5':
            lda_model = models.LdaModel.load('divorce3/lda.model')
            text2vec = corpora.Dictionary.load('divorce3/lda.dct')
            roughRes = rough.getIndexListbyLda(3, lda_model, text2vec)
            res['res'] = gettestresult(roughRes, "lda", col2, referenceStandard)
        elif option == '6':
            lda_model = models.LdaModel.load('divorce3/lda.model')
            text2vec = corpora.Dictionary.load('divorce3/lda.dct')
            roughRes = rough.getIndexListbyLda(4, lda_model, text2vec)
            res['res'] = gettestresult(roughRes, "LDA", col2, referenceStandard)

        col3.insert(res)
    cur.close()
    logging.info('finish!')

if __name__ == '__main__':
    # tag = input("tag: 2:验证集，3测试集, 4..")
    # option = input("option： 1.tfidf 2.weightedTfidf 3.lda(vec上下浮动)\n\
    #         4.lda(dis，direct浮动)  5.lda（最大topic浮动）6.lda(遍历所有) 7.doc2vec")
    #test(tag, option)
    # s1 = time.time()
    # test('2', '4')
    # s2 = time.time()
    # print("24finish, cost: %.3f" % s2-s1)

    # s1 = time.time()
    # test('3', '4')
    # s2 = time.time()
    # print("34finish, cost: ", s2-s1)

    s1 = time.time()
    test('4', '4')
    s2 = time.time()
    print("44finish, cost: ", s2 - s1)

    s1 = time.time()
    test('2', '5')
    s2 = time.time()
    print("25finish, cost: ", s2-s1)

    s1 = time.time()
    test('3', '5')
    s2 = time.time()
    print("35finish, cost: ", s2-s1)

    s1 = time.time()
    test('4', '5')
    s2 = time.time()
    print("45finish, cost: ", s2-s1)

    s1 = time.time()
    test('2', '6')
    s2 = time.time()
    print("26finish, cost: ", s2-s1)

    s1 = time.time()
    test('3', '6')
    s2 = time.time()
    print("36finish, cost: ", s2-s1)

    s1 = time.time()
    test('4', '6')
    s2 = time.time()
    print("46finish, cost: ", s2 - s1)