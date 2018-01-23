from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *

from jieba import posseg

def token(id, paragraph):
    tokenRes = list()
    flagRes = list()

    for word,flag in posseg.cut(paragraph):
        tokenRes.append(word)
        flagRes.append(flag)

    return Row(lawcaseid = id, token = (' ').join(tokenRes), flag = (' ').join(flagRes))


if __name__ == '__main__':
    my_spark = SparkSession \
        .builder \
        .appName("myApp") \
        .master("spark://192.168.68.11:7077") \
        .config("spark.driver.host", "192.168.68.11") \
        .config("spark.mongodb.input.uri", "mongodb://192.168.68.11:20000/lawCase.lawcase") \
        .config("spark.mongodb.input.partitioner", "MongoShardedPartitioner") \
        .config("spark.mongodb.output.uri", "mongodb://192.168.68.11:20000/wxdb.lawcasetokenjieba") \
        .getOrCreate()


    # field_list_read = ['_id', 'text']
    # fields_read = [StructField(field, StringType(), True) for field in field_list_read]
    # schema_read = StructType(fields_read)
    pipeline = "{'$limit' : 5}"
    #collection = ctx.read.schema(schema_read).format("com.mongodb.spark.sql").options(uri="mongodb://192.168.68.11:20000/lawCase.codeofca").option("pipeline", pipeline).load()
    collection = my_spark.read.format("com.mongodb.spark.sql").option("uri", "mongodb://192.168.68.11:20000/lawCase.lawcase").option("pipeline", pipeline).load()

    collection.show()

    case_rdd = collection.rdd
    words_rdd = case_rdd.map(lambda s: token(s['_id'], s['text']))

    res = my_spark.createDataFrame(words_rdd)
    res.createOrReplaceTempView("words_rdd")
    res.show()
    res.write.format("com.mongodb.spark.sql.DefaultSource")\
        .mode("append").option("database","wxdb")\
       .option("collection","lawcasetokenjieba").save()