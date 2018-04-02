from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec


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



    #pipeline = "{'$limit' : 5}"
    #collection = my_spark.read.format("com.mongodb.spark.sql").option("uri", "mongodb://192.168.68.11:20000/lawCase.AJsegment").option("pipeline", pipeline).load()
    collection = my_spark.read.format("com.mongodb.spark.sql").option("uri", "mongodb://192.168.68.11:20000/lawCase.AJsegment").load()

    #collection.show()

    case_rdd = collection.rdd.map(lambda s: s['ldasrc'].split(" ").toseq())

    word2val = Word2Vec(vectorSize=100)
    model = word2val.fit(case_rdd)

    result = model.getVectors()
    result.show()

    res = my_spark.createDataFrame(model)

    res.createOrReplaceTempView("vec_rdd")
    res.show()

    res.write.format("com.mongodb.spark.sql.DefaultSource")\
        .mode("append").option("database","lawCase")\
       .option("collection","AJvec").save()