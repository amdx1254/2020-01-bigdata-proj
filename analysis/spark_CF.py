#!/usr/bin/env python
# coding: utf-8

from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udf, lit

import pyspark.sql.functions as sql_func
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.mllib.evaluation import RegressionMetrics, RankingMetrics
from pyspark.ml.evaluation import RegressionEvaluator

import pyspark.sql.functions as F

from pyspark.sql.functions import col

sc = SparkContext('')
spark = SparkSession(sc)
sqlContext = SQLContext(sc)


def dividePrice(totalAmount):
    if totalAmount == '###':
        totalAmount = 0
    price = int(totalAmount)
    if 0 <= price and price <30000:
        return 0.5
    elif 30000<= price and price <50000:
        return 1.0
    elif 50000<= price and price <70000:
        return 1.5
    elif 70000<= price and price <100000:
        return 2.0
    elif 100000<= price and price <200000:
        return 2.5
    elif 200000<= price and price< 300000:
        return 3.0
    elif 300000<= price and price <400000:
        return 3.5
    elif 400000<= price and price <500000:
        return 4.0
    else:
        return 5.0


wadiz_schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("funding_id", IntegerType()),
    StructField("funding_name", StringType()),
    StructField("category", StringType()),
    StructField("backedAmount", StringType())
])

backed_udf = udf(dividePrice, DoubleType())

final_stat =  spark.read.option("escape", "\"").csv("users.csv", header=True, inferSchema=True, schema=wadiz_schema)
final_stat = final_stat.filter(final_stat.backedAmount != "0")
final_stat = final_stat.filter(final_stat.backedAmount != "###")
final_stat = final_stat.withColumn("backedAmount", backed_udf(final_stat["backedAmount"]))

final_stat.show()
print(final_stat.count())



ratings = (final_stat
    .select(
        'user_id',
        'funding_id',
        'backedAmount',
    )
)

ratings.filter("user_id is NULL").show()



(training, test) = ratings.randomSplit([0.8, 0.2], seed=13)
training.show()
test.show()




# Build the recommendation model using ALS on the training data
# Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
als = ALS(rank=50, maxIter=20, regParam=0.01, 
          userCol="user_id", itemCol="funding_id", ratingCol="backedAmount",
          coldStartStrategy="drop",
          implicitPrefs=False)
model = als.fit(training)

# Evaluate the model by computing the RMSE on the test data
predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="backedAmount",
                                predictionCol="prediction")

rmse = evaluator.evaluate(predictions)
print("Root-mean-square error = " + str(rmse))


userRecs = model.recommendForAllUsers(10)



userRecs = userRecs.select("*", F.explode("recommendations").alias("exploded_data"))
userRecs = userRecs.withColumnRenamed(
            "user_id",
            "input_id"
        )

userRecs = userRecs.withColumn(
            "id",
            F.col("exploded_data").getItem("funding_id")
        )

userRecs = userRecs.withColumn(
            "score",
            F.col("exploded_data").getItem("rating")
        )


userRecs = userRecs.select("id", "score", "input_id").filter(userRecs.score > 0.0).filter(userRecs.score < 1.0)


import csv
import ast
import pyspark.sql.functions as F

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

from pyspark.sql.types import *
from pyspark.sql.functions import udf, lit

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

# input: 추천 상품 (input_id, id, score) > output: inner join (input_id, id, score, name, category, makerName, summary)
def getProductDetails(in_product):
    a = in_product.alias("a")
    b = spark_df.alias("b")
    
    return a.join(b, col("a.id") == col("b.id"), 'inner') \
             .select([col('a.'+xx) for xx in a.columns] + [col('b.name'),col('b.category'),
                                                           col('b.makerName'),col('b.summary'),
                                                          col('b.rangeAmount'), col('b.amount')])                                                       
sims = getProductDetails(userRecs)
sims = sims.withColumnRenamed('input_id', 'user_id')
sims = sims.select('user_id','id','name','category', 'amount','score').orderBy('score', ascending=False).limit(10)
sims.toPandas().to_json('./users_CF_test.json', orient='table')
