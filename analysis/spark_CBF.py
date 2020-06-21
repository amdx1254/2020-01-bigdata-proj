#!/usr/bin/env python
# coding: utf-8

from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import *

sc = SparkContext('')
spark = SparkSession(sc)
sqlContext = SQLContext(sc)

import csv
import ast
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import udf, lit
from pyspark.ml.feature import Tokenizer,HashingTF, Word2Vec
wadiz_schema = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("category", StringType()),
    StructField("makerName", StringType()),
    StructField("summary", StringType()),
    StructField("achievementRate", IntegerType()),
    StructField("totalAmount", IntegerType()),
    StructField("totalSupporter", IntegerType()),
    StructField("totalLike", IntegerType()),
    StructField("rewardSatisfaction", DoubleType()),
    StructField("makerSatisfaction", DoubleType()),
    StructField("detailUrl", StringType()),
    StructField("campaigncomments", StringType()),
    StructField("comments", StringType())
])
spark_df =  spark.read.option("multiline",'true').csv("wadiz.csv", header=True, inferSchema=True, schema=wadiz_schema)


def summary_type(summary):
    if(summary is None):
        return '0'
    else:
        return summary.replace('\n', '')

def makerName_type(makerName):
    if(makerName is None):
        return '0'
    else:
        return makerName
    
def category_type(category):
    if(category is None):
        return '0'
    else:
        return category    

summary_udf = udf(summary_type, StringType())  
makerName_udf = udf(makerName_type, StringType())  
category_udf = udf(category_type, StringType())  
soop = udf(lambda category, makerName, summary: (category)*2 + (makerName + ' ')*2 + summary)
spark_df = spark_df.withColumn("id", spark_df['id'].cast('integer'))
spark_df = spark_df.withColumn("summary", summary_udf(spark_df['summary']))
spark_df = spark_df.withColumn("makerName", makerName_udf(spark_df['makerName']))
spark_df = spark_df.withColumn("category", category_udf(spark_df['category']))
spark_df = spark_df.withColumn("achievementRate", spark_df['achievementRate'].cast('integer'))
spark_df = spark_df.withColumn("totalAmount", spark_df['totalAmount'].cast('integer'))
spark_df = spark_df.withColumn("totalSupporter", spark_df['totalSupporter'].cast('integer'))
spark_df = spark_df.withColumn("totalLike", spark_df['totalLike'].cast('integer'))
spark_df = spark_df.withColumn("soop", soop(spark_df['category'], spark_df['makerName'], spark_df['summary']).cast('string'))

def dividePrice(totalAmount, totalSupporter):
    if(totalSupporter is None or totalAmount is None):
        return 0
    if (totalSupporter == 0 or totalAmount == 0):
        return 0
    
    price = int(totalAmount / totalSupporter)
    if 0 <= price and price <30000:
        return 0
    elif 30000<= price and price <50000:
        return 1
    elif 50000<= price and price <70000:
        return 2
    elif 70000<= price and price <100000:
        return 3
    elif 100000<= price and price <200000:
        return 4
    elif 200000<= price and price< 300000:
        return 5
    elif 300000<= price and price <400000:
        return 6
    elif 400000<= price and price <500000:
        return 7
    else:
        return 8
    
def divideAmount(totalAmount, totalSupporter):
    if(totalSupporter is None or totalAmount is None):
        return 0
    if (totalSupporter == 0 or totalAmount == 0):
        return 0
    price = int(totalAmount / totalSupporter)
    return price
    
price_udf = udf(dividePrice, IntegerType())
amount_udf = udf(divideAmount, IntegerType())
spark_df = spark_df.withColumn('rangeAmount', price_udf(spark_df['totalAmount'], spark_df['totalSupporter']))
spark_df = spark_df.withColumn('amount', amount_udf(spark_df['totalAmount'], spark_df['totalSupporter']))
spark_df = spark_df.withColumn('soop', spark_df['soop'].cast('string'))
spark_df.show()

tokenizer = Tokenizer(inputCol='soop', outputCol='keywords')
wordData = tokenizer.transform(spark_df)
word2Vec = Word2Vec(vectorSize=100, minCount=5, inputCol='keywords', outputCol='word_vec', seed=123)
word2VecData = word2Vec.fit(wordData)
word2VecData = word2VecData.transform(wordData)

# rangeAmount 비교값 추가
all_wadiz_vecs = word2VecData.select('id','word_vec','rangeAmount')


import pyspark.sql.functions as F
from pyspark.sql.functions import col
from pyspark.ml.feature import Normalizer
from pyspark.sql.column import Column, _to_java_column, _to_seq 

def cosinesimilarity_udf(a, b): 
    cosinesimilarityUDF = spark._jvm.cosinesimilarityUDFs.cosinesimilarityUDF() 
    return Column(cosinesimilarityUDF.apply(_to_seq(spark.sparkContext, [a, b], _to_java_column)))

# input: 상품 id 리스트 > output: 추천 상품 (input_id(입력한 상품 id), id(입력한 상품과 코사인 유사도가 제일 높은 상품 id), score(코사인 유사도 계산)))
def getSimilarProduct(w_ids, sim_product_limit=10):
    all_wadiz_vecs_wids = all_wadiz_vecs.where(all_wadiz_vecs.id.isin(w_ids))
    all_wadiz_no_wids = all_wadiz_vecs.filter(~all_wadiz_vecs.id.isin(w_ids))
    all_wadiz_vecs_renamed = all_wadiz_no_wids.select(F.col('id').alias('id2'), F.col('word_vec').alias('word_vec2'), F.col('rangeAmount').alias('rangeAmount2'))
    all_wadiz_vecs_joined = all_wadiz_vecs_wids.join(all_wadiz_vecs_renamed,[all_wadiz_vecs_renamed.rangeAmount2 > all_wadiz_vecs_wids.rangeAmount - 2,all_wadiz_vecs_renamed.rangeAmount2  < all_wadiz_vecs_wids.rangeAmount + 2] ,'inner')
    all_wadiz_vecs_joined = all_wadiz_vecs_joined.withColumn('score', cosinesimilarity_udf(all_wadiz_vecs_joined.word_vec,all_wadiz_vecs_joined.word_vec2)).select(F.col('id2').alias('id'), F.col('score'), F.col('id').alias('input_id'))
    all_wadiz_vecs_joined = all_wadiz_vecs_joined.na.fill(0.0, 'score').filter(F.col('score') < 1.0).filter(F.col('score')>0.0)
     
    return all_wadiz_vecs_joined

# input: 추천 상품 (input_id, id, score) > output: inner join (input_id, id, score, name, category, makerName, summary)
def getProductDetails(in_product):
    a = in_product.alias("a")
    b = spark_df.alias("b")
    
    return a.join(b, col("a.id") == col("b.id"), 'inner').select([col('a.'+xx) for xx in a.columns] + [col('b.name'),col('b.category'),
                                                           col('b.makerName'),col('b.summary'),
                                                          col('b.rangeAmount'), col('b.amount')])                                                       


# ### User based Recomment
user_df =  spark.read.csv("users.csv", header=True, inferSchema=True)

user_df.select('user_id' ,'funding_id').show()
user_df.printSchema()

from pyspark.sql import Row
user_rdd = user_df.groupby('user_id').agg(F.collect_list('funding_id').alias('funding_ids')).rdd.collect()

for i, r in enumerate(user_rdd):
    u_id = r[0]
    funding_ids = list(r[1])
    print(i, u_id, funding_ids)
    sims = getProductDetails(getSimilarProduct(list(set(funding_ids))))
    sims = sims.withColumn('user_id', lit(u_id))
    sims = sims.select('user_id','id','name','category', 'amount','score').orderBy('score', ascending=False).limit(10)
    if(i == 0):
        allSims = sims
    else:
        allSims = allSims.union(sims)
        
    if(i == len(user_rdd)-1):
        allSims.toPandas().to_json('./users_CBF_test.json', orient='table')        




