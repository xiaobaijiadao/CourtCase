from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
import pymongo
from bson.objectid import ObjectId

from jieba import posseg

dictionary = dict()
con = pymongo.MongoClient('localhost', 27017)
lenth = 0
for item in con.Lawcase.dictionary.find(no_cursor_timeout = True):
    dictionary[item['word']] = item['pos']
    lenth += 1

def getVec(id, ldasrc):
    words = ldasrc.strip().split(' ')
    sparseVec = dict()

    for word in words:
        if word != None:
            if dictionary[word] in sparseVec:
                sparseVec[dictionary[word]] += 1
            else:
                sparseVec[dictionary[word]] = 1

    return Row(lenth = lenth,  pos = (' ').join(sparseVec.keys()), flag = (' ').join(sparseVec.values()))


if __name__ == '__main__':
    my_spark = SparkSession \
        .builder \
        .appName("myApp") \
        .master("spark://192.168.68.11:7077") \
        .config("spark.driver.host", "192.168.68.11") \
        .config("spark.mongodb.input.uri", "mongodb://192.168.68.11:20000/lawCase.AJsegment") \
        .config("spark.mongodb.input.partitioner", "MongoShardedPartitioner") \
        .config("spark.mongodb.output.uri", "mongodb://192.168.68.11:20000/lawCase.AJvec") \
        .getOrCreate()


    # field_list_read = ['_id', 'text']
    # fields_read = [StructField(field, StringType(), True) for field in field_list_read]
    # schema_read = StructType(fields_read)
    pipeline = "{'$limit' : 5}"
    #collection = ctx.read.schema(schema_read).format("com.mongodb.spark.sql").options(uri="mongodb://192.168.68.11:20000/lawCase.codeofca").option("pipeline", pipeline).load()
    collection = my_spark.read.format("com.mongodb.spark.sql").option("uri", "mongodb://192.168.68.11:20000/lawCase.AJsegment").option("pipeline", pipeline).load()

    collection.show()

    case_rdd = collection.rdd
    vec_rdd = case_rdd.map(lambda s: getVec(s['fulltext'], s['ldasrc']))

    res = my_spark.createDataFrame(vec_rdd)
    res.createOrReplaceTempView("vec_rdd")
    res.show()
    res.write.format("com.mongodb.spark.sql.DefaultSource")\
        .mode("append").option("database","lawCase")\
       .option("collection","AJvec").save()