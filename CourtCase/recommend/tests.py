from django.test import TestCase
import pymongo
from gensim import corpora, models


def getRateByName(col, option):
    if option not in ['precision', 'recall', 'f-measure']:
        print("option error!")
        return None

    res = [[], [], [], []]
    i = 0
    for item in col.find():
        res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount5'])
        res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount10'])
        res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount20'])
        res[i * 2].append(item[option]['resStaByKeyWord']['simple']['covercount50'])
        res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount5'])
        res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount10'])
        res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount20'])
        res[i * 2].append(item[option]['resStaByTfidf']['simple']['covercount50'])
        res[i * 2].append(item[option]['resStaByLda']['simple']['covercount5'])
        res[i * 2].append(item[option]['resStaByLda']['simple']['covercount10'])
        res[i * 2].append(item[option]['resStaByLda']['simple']['covercount20'])
        res[i * 2].append(item[option]['resStaByLda']['simple']['covercount50'])
        res[i * 2].append(item[option]['resStaByTest']['simple']['covercount5'])
        res[i * 2].append(item[option]['resStaByTest']['simple']['covercount10'])
        res[i * 2].append(item[option]['resStaByTest']['simple']['covercount20'])
        res[i * 2].append(item[option]['resStaByTest']['simple']['covercount50'])

        res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount5'])
        res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount10'])
        res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount20'])
        res[i * 2 + 1].append(item[option]['resStaByKeyWord']['simple']['covercount50'])
        res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount5'])
        res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount10'])
        res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount20'])
        res[i * 2 + 1].append(item[option]['resStaByTfidf']['simple']['covercount50'])
        res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount5'])
        res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount10'])
        res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount20'])
        res[i * 2 + 1].append(item[option]['resStaByLda']['simple']['covercount50'])
        res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount5'])
        res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount10'])
        res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount20'])
        res[i * 2 + 1].append(item[option]['resStaByTest']['simple']['covercount50'])
        i += 1
    return res

if __name__ =="__main__":
    con = pymongo.MongoClient("192.168.68.11", 20000)
    #
    # col1 = con.divorceCase.LDAvec
    # col2 = con.divorceCase.AJsegment
    #
    # lda = models.LdaModel.load('lda.model')
    # dic = corpora.Dictionary.load('lda.dct')
    #
    # text = col2.find_one({"fullTextId": "5a34481f0e2c810b3cc2f90a"})['ldasrc'].strip().split(' ')
    # print(lda[dic.doc2bow(text)])
    # print(col1.find_one({"fullTextId": "5a34481f0e2c810b3cc2f90a"})['dis'])
    col3 = con.divorceCase3.searchStatutePerformValidateEvaluate
    for item in getRateByName(col3, 'precision'):
        print(item)
