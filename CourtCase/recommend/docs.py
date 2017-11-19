#mongodb连接接口
import pymongo


class Dao:

    def __init__(self, host='localhost', port=27017, user='', pwd=''):
        self.conn = pymongo.MongoClient()

    def getCollection(self, db, collection):
        self.col = self.conn[db][collection]

    def findByKey(self, key, value):
        return self.col.find({key: value})

# if __name__ == '__main__':
#     d = Dao()
#     d.getCollection('caseTest', 'indexTable')
#     for item in d.findByKey('key', 'nv'):
#         print(item)