import pymongo
from .dao import Dao

class indexTable:
    def __init__(self):
        self.dao = Dao()
        self.dao.getCollection("Lawcase", "indexTable")

    def getAllDoc(self):
        return self.dao.getAll()

    def getCaselistByKey(self, word):
        res = dict()
        for item in self.dao.findByKey(key= "key", value= word):
            for case in item["caselist"]:
                cs = dict()
                cs["tfidf"] = case["tfidf"]
                cs["wordsCount"] = 1
                res[case["caseid"]] = cs
        return res

class paragraph:
    def __init__(self):
        self.dao = Dao()
        self.dao.getCollection("Lawcase", "paragraph")

    def getAllDoc(self):
        return self.dao.getAll()

    def getAJJBQKBy_Id(self, word):
        res = ""
        item = self.dao.getByKey(key= "_id", value= word)

        litigationRecord = "" if item["litigationRecord"] == "" else item["litigationRecord"]["text"]
        defendantArgued = "" if item["defendantArgued"] == "" else item["defendantArgued"]["text"]
        factFound = "" if item["factFound"] == "" else item["factFound"]["text"]

        res = litigationRecord + defendantArgued + factFound
        print(res)

        return res

    def getDisplayInfoBy_Id(self, word):
        res = dict()
        item = self.dao.getByKey(key="_id", value=word)

        res["plain"] = "" if item["litigationRecord"] == "" else item["litigationRecord"]["text"]
        res["defendantArgued"] = "" if item["defendantArgued"] == "" else item["defendantArgued"]["text"]
        res["factFound"] = "" if item["factFound"] == "" else item["factFound"]["text"]
        res["analysisProcess"] = "" if item["analysisProcess"] == "" else item["analysisProcess"]["text"]
        res["caseDecision"] = "" if item["caseDecision"] == "" else item["caseDecision"]["text"]

    def getInfo(self, word):
        item = self.dao.getByKey(key="_id", value=word)
        return item

class lawcase:
    def __init__(self):
        self.dao = Dao()
        self.dao.getCollection("Lawcase", "lawcase")

    def getInfo(self, word):
        item = self.dao.getByKey(key="_id", value=word)
        return item