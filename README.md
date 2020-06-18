# 2020-01-group2

### Repository Structure
  1. Crawling.py
  2. Spark_CF.ipynb
  3. Spark_CBF.ipynb
  4. Web

### Software Require
  1. Jupyter notebook
  2. Python


### Algorithms implemented and evaluated
  1. Collaborative Filtering
  2. Content based Filtering


# Implementation

## DataAcquisition
 ### Crawling
- Crawling Data:
  1) Funding Data :  productId, name, category, makerName, summary, achievementRate, summary, totalAmount, totalSupporter, totalLike, rewardSatisfaction, makerSatisfaction, comments, campaignComments, detailUrl
  2) User Data: userId, fundingList(fundingId)


```
dfProduct = dfProduct.append({
                'id': id,
                'name': name,
                'category': category,
                'makerName': makerName,
                'summary' : summary,
                'achievementRate': achievementRate,
                'totalAmount': totalAmount,
                'totalSupporter': int(totalSupporter),
                'totalLike': int(totalLike),
                'rewardSatisfaction': rewardSatisfaction, 
                'makerSatisfaction': makerSatisfaction,
                'comments': comments,
                'campaigncomments': campaigncomments, # 응원댓글 
                'participants': participants, # 참여자
                'detailUrl': detailUrl,
                },ignore_index=True)
```



## DataPreprocessing


## DataAnalysis
### Collaborative Filtering
- Using PySpark AST Module
- Input : ```[[userid1, fundingid1, backedAmount1], [userid2, fundingid2, backedAmount2],...]```
- Output : 
```[userid, [[Funding_ID1, Score1], [Funding_ID2, Score2],...]```

### Content Based Filtering
- Considered Feature
  - name
  - makerName 
  - summary
  - category
  - totalAmount
  - totalSupporter

- Preprocessing Feature
  - makerName, summary, category
    - Tokenizer
    - Word2Vec
    - CosineSimiliarity

  - rangeAmount, totalAmount, totalSupporter
    - 0~8 range amount
    - filter range amount  

```
spark_df = spark_rdd.toDF()
tokenizer = Tokenizer(inputCol='soop', outputCol='keywords')
wordData = tokenizer.transform(spark_df)
word2Vec = Word2Vec(vectorSize=100, minCount=5, inputCol='keywords', outputCol='word_vec', seed=123)
word2VecData = word2Vec.fit(wordData)
word2VecData = word2VecData.transform(wordData)
word2VecData_rdd = word2VecData.rdd
```


## DataVisualization
### Tech
- Language: JavaSctripts
- Backend: Express
- Frontend: ejs, chartjs, jQuery, Ajax

### filtering.js
 - GET: cf
   - input: user_id
   - output: user_id의 Collaborative filtering Result
 - GET: cbf
   - input: user_id
   - output: user_id의 Content Based filtering Result

### index.ejs
 - item: Collaborative filtering, Content Based filtering 결과 아이템의 이름, 평균 펀딩 가격, Score
 - Score Chart: X축 결과 아이템들의 ID, Y축 아이템별 Score
 - Category Chart: X축 결과 아이템들의 카테고리, Y축 카테고리별 Count
 - Amount Chart: X축 가격의 범위, Y축 가격 범위 별 Count

# Install

```sh
$ cd web
$ npm install
$ npm start
```
