# 2020-01-group2

# DataAcquisition
## Crawling
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



# DataPreprocessing


# DataAnalysis
## Scala
- PySpark Cosine Similarity UDF Optimization
#### Build
```sh
$ cd scala
$ sbt package
```
- Use ```--jar``` parameter to use in spark


# DataVisualization
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
