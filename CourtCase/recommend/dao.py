#mongodb连接接口
import pymongo
from bson.objectid import ObjectId

class Dao:

    def __init__(self, host='localhost', port=27017, user='', pwd=''):
        self.conn = pymongo.MongoClient()

    def getCollection(self, db, collection):
        self.col = self.conn[db][collection]

    def findByKey(self, key, value):
        if self.col.find({key: value}).count()>0:
            return self.col.find({key: value})
        return dict()

    def getByKey(self, key, value):
        if key == "_id":
            return self.col.find_one({key: ObjectId(value)})
        return self.col.find_one({key: value})

    def getAll(self):
        return self.col.find()

# if __name__ == '__main__':
#     d = Dao()
#     d.getCollection('caseTest', 'indexTable')
#     for item in d.findByKey('key', 'nv'):
#         print(item)