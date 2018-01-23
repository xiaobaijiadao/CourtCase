from gensim import corpora, models, similarities
import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt
import pymongo, logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='lda.log',
                filemode='w')

def getDataFromMongo(col):
    caseList = list()
    idList = list()
    # i = 1
    for item in col.find():
        words = item['ldasrc'].strip().split(' ')
        caseList.append(words)
        idList.append(item['fulltextid'])
        # i += 1
        # if i > 1000:
        #     break

    return caseList,idList

def getDis(doc_topics, num_topics):
    disList = list()
    for doc in doc_topics:
        i = 0
        dis = list()
        for j in range(num_topics):
            if i < len(doc):
                if doc[i][0] == j:
                    dis.append(float(doc[i][1]))
                    i += 1
                else:
                    dis.append(0.0)
            else:
                dis.append(0.0)
        disList.append(dis)
    return disList

def write2mongo(col, idList, disList):
    for id,dis in zip(idList, disList):
        print(id, dis)
        col.insert({
            "fullTextId" : id,
            "dis" : dis,
        })


if __name__ == '__main__':
    con = pymongo.MongoClient('192.168.68.11', 20000)
    col1 = con.divorceCase.AJsegment
    col2 = con.divorceCase.LDAvec

    print("enter mongo")
    caselist,idlist = getDataFromMongo(col1)
    print("out mongo")
    print("calist lenth: %d" % len(caselist))

    print('build dictionary')
    dictionary = corpora.Dictionary(caselist)
    dict_len = len(dictionary)
    # transform the whole texts to sparse vector
    corpus = [dictionary.doc2bow(case) for case in caselist]
    print(len(corpus))

    print('build lda')
    num_topics = 6
    # create a transformation, from tf-idf model to lda model
    lda = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary,
          alpha=0.01, eta=0.01, minimum_probability=0.001, update_every = 1, chunksize = 100, passes = 1)
    print('out lda')
    lda.save('lda.model')

    doc_topics = lda.get_document_topics(corpus)

    dislist = getDis(doc_topics, num_topics)

    print(len(idlist), len(dislist))
    write2mongo(col2, idlist, dislist)


    num_show_term = 10   # 每个主题下显示几个词
    for topic_id in range(num_topics):
        logging.info('第%d个主题的词与概率如下：\t' % topic_id)
        term_distribute_all = lda.get_topic_terms(topicid=topic_id)
        term_distribute = term_distribute_all[:num_show_term]
        term_distribute = np.array(term_distribute)
        term_id = term_distribute[:, 0].astype(np.int)
        logging.info('词：\t')
        for t in term_id:
            logging.info(dictionary.id2token[t])
        logging.info('\n概率：\t', term_distribute[:, 1])


    # mpl.rcParams['font.sans-serif'] = [u'SimHei']
    # mpl.rcParams['axes.unicode_minus'] = False
    # for i, k in enumerate(range(num_topics)):
    #     ax = plt.subplot(2, 3, i+1)
    #     item_dis_all = lda.get_topic_terms(topicid=k)
    #     item_dis = np.array(item_dis_all[:num_show_term])
    #     ax.plot(range(num_show_term), item_dis[:, 1], 'b*')
    #     item_word_id = item_dis[:, 0].astype(np.int)
    #     word = [dictionary.id2token[i] for i in item_word_id]
    #     ax.set_ylabel(u"概率")
    #     for j in range(num_show_term):
    #         ax.text(j, item_dis[j, 1], word[j], bbox=dict(facecolor='green',alpha=0.1))
    # plt.suptitle(u'10个主题及其10个主要词的概率', fontsize=18)
    # plt.show()


    # for i in range(9):
    #     ax = plt.subplot(3, 3, i + 1)
    #     print(doc_topics[i])
    #     doc_item = np.array(doc_topics[i])
    #     print(doc_item)
    #     doc_item_id = np.array(doc_item[:, 0])
    #     print(doc_item_id)
    #     doc_item_dis = np.array(doc_item[:, 1])
    #     print(doc_item_dis)
    #     ax.plot(doc_item_id, doc_item_dis, 'r*')
    #     for j in range(doc_item.shape[0]):
    #         ax.text(doc_item_id[j], doc_item_dis[j], '%.3f' % doc_item_dis[j])
    # plt.suptitle(u'前9篇文档的主题分布图', fontsize=18)
    # plt.show()