import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

import random
import time, os

import re
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rc

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
user_data = {'userName' : 'amdx1254@naver.com', 'password': '1q2w3e4r!'}
count = 1

# 함수이름: product_detail
# 동작: 디테일한 상품 정보 페이지에 접속해서 상품정보요약, 좋아요, 서포터 수를 크롤링해온다.
# 크롤러동작사이트: https://www.wadiz.kr/web/campaign/detail/{product Id}
# 입력값: productId,  detailUrl
# 출력값: summary, totalLike, totalSupporter / 상품정보요약, 전체좋아요수, 전체서포터수(펀딩한사람 수)
# 출력값 예시: 
    #summary: 음악이 들리는 선글라스 정글 팬써 (Zungle Panther), 정글 팬써와 함께...	
    #totalLike: 1865
    #totalSupporter: 7669
# 로딩 예외처리는 아직 진행하지 않음
def product_detail(id, detailUrl):
    # requests모듈로 직접 가져
    res = requests.get(detailUrl, headers=headers).text
    soup = bs(res, 'html.parser')
    
    try:
        summary = soup.find('div', class_='campaign-summary').text
        totalSupporter = soup.find('p', class_='total-supporter').text.replace('명의 서포터','').replace(',','')
        #totalSupporter = driver.find_element_by_class_name('total-supporter').text.replace('명의 서포터','').replace(',','')
        totalLike = soup.find('em', class_='cnt-like').text.replace(',','')
        # totalLike = driver.find_element_by_class_name('cnt-like').text.replace(',','')
    except:
        summary = '0'
        totalSupporter = '0'
        totalLike = '0'              
    return summary, totalSupporter, totalLike



# 함수이름: product_comment
# 동작: 상품의 댓글 정보, 점수?평점?를 크롤링해온다. 
# 크롤러동작사이트(점수) : https://www.wadiz.kr/web/reward/api/satisfactions/campaigns/{id}/aggregate
# 크롤러동작사이트(댓글) : https://www.wadiz.kr/web/reward/api/satisfactions?campaignId={id}&orderProperty=REGISTERED&direction=desc&page={comment_page}&size=5
# 입력값: productId
# 출력값: rewardSatisfacation, makerSatisfaction, comments
    #rewardSatisfaction: 4.4
    #makerSatisfaction: 4.7
    #comments: [['4', ' 편안 하게 잘 쓰고 있어요'], ['5', ' 수납이나 등에 멜때...]]
def product_comment(id):
    # 상품 점수 관련 api사이
    aggregate_url = f"https://www.wadiz.kr/web/reward/api/satisfactions/campaigns/{id}/aggregate"
    comments = []
    try:
        aggregate_data = requests.get(aggregate_url, headers=headers).json()
        rewardSatisfaction = aggregate_data['data']['aggregatesByItem'][1]['averageScore']
        makerSatisfaction = aggregate_data['data']['aggregatesByItem'][0]['averageScore']
        
        if (rewardSatisfaction == None):
            rewardSatisfaction = None
            makerSatisfaction = None
            productComments = None
            print('Cannot find reviews...')
            return rewardSatisfaction, makerSatisfaction, comments
    except:
        rewardSatisfaction = None
        makerSatisfaction = None
        productComments = None
        print('Cannot find reviews...')
        return rewardSatisfaction, makerSatisfaction, comments

    #  satisfaction comment 주소.
    # campaignId : 상품 ID
    # page: comment page
    # size: 한번에 몇개씩 가져올지
    comment_page = 0
    comment_url = f"https://www.wadiz.kr/web/reward/api/satisfactions?campaignId={id}&orderProperty=REGISTERED&direction=desc&page={comment_page}&size=5"
    productComments = requests.get(comment_url, headers=headers).json()['data']['content'] # json형태로 가져오고 data->content에 댓글내용 존

    # 댓글이 존재하지 않을때까지 page수를 하나씩 증가시키며 가져온다.
    while len(productComments) != 0:
        time.sleep(random.uniform(1,3))
        for productComment in productComments:
            commentRating = productComment['averageScore']
            comment = productComment['comment']
            comments.append([commentRating, comment])
        comment_page = comment_page + 1
        comment_url = f"https://www.wadiz.kr/web/reward/api/satisfactions?campaignId={id}&orderProperty=REGISTERED&direction=desc&page={comment_page}&size=5"
        productComments = requests.get(comment_url, headers=headers).json()['data']['content']
    return rewardSatisfaction, makerSatisfaction, comments



# 함수이름: product_comment2
# 동작: 응원댓글 정보를 가져온다.
# 크롤러동작사이트: https://www.wadiz.kr/web/campaign/detail/qa/{product Id}
# 입력값: productId
# 출력값: comments
    #comments: [편안 하게 잘 쓰고 있어요', ' 수납이나 등에 멜때...]
def product_comment2(id):
    # 댓글 가져오는 것은 product_comment함수와 유사함.
    comments = []
    comment_page = 0
    comment_url = f"https://www.wadiz.kr/web/reward/api/comments/campaigns/{id}?page={comment_page}&size=15&commentGroupType=CAMPAIGN"
    productComments = requests.get(comment_url, headers=headers).json()['data']['content']
    
    while len(productComments) != 0:
        time.sleep(random.uniform(1,3))
        for productComment in productComments:
            boardId = productComment['boardId']
            comment = productComment['body']
            comments.append([boardId, comment])
        comment_page = comment_page + 1
        comment_url = f"https://www.wadiz.kr/web/reward/api/comments/campaigns/{id}?page={comment_page}&size=15&commentGroupType=CAMPAIGN"
        productComments = requests.get(comment_url, headers=headers).json()['data']['content']
    return comments


# 함수이름: get_realuserid
# 동작: encUserId에 기반하여 실제 userid를 가져온다.
# 입력값: encUserId
# 출력값: realUserId
def get_realuserid(encUserId):
    td_list = []
    int_encUserId = int(encUserId)

    # encUserId의 약수 구해서 td_list에 넣음
    for i in range(1, int(int_encUserId**0.5)+1):
        if (int_encUserId % i == 0):
            td_list.append(i)
            if i != int_encUserId // i:
                td_list.append(int_encUserId // i)
    td_list.sort()
    # 약수 중 100으로 나누어 1의 나머지가 나오는 값중 가장 큰 값이 실제 userId
    realUserId = 0
    for i in td_list:
        if i % 100 == 1:
            realUserId = i
    return str(realUserId)
                   

# 함수이름: get_participants
# 동작: 펀딩 참여자 리스트를 가져온다. 
# 크롤러동작사이트: https://www.wadiz.kr/web/campaign/ajaxParticipationList?campaignId={id}&pageSize=100000&startNum=0
# 입력값: productId
# 출력값: [유저id, 닉네임, 가격]
def get_participants(id):
    participant_list = []
    time.sleep(random.uniform(1,3))
    participants_url = f"https://www.wadiz.kr/web/campaign/ajaxParticipationList?campaignId={id}&pageSize=100000&startNum=0"
    participants = requests.get(participants_url, headers=headers).json()['participationList']
    for participant in participants:
        if participant['encIntUserId'] == '###':
            continue
        encUserId = participant['encUserId']
        realUserId = get_realuserid(encUserId)
        nickName = participant['nickName']
        backedAmount = participant['backedAmount']
        participant_list.append([realUserId, nickName ,backedAmount])
        
    return participant_list


# 함수이름: get_user_fundinglist
# 동작: 유저의 펀딩 리스트를 가져온다.. 
# 크롤러동작사이트: https://www.wadiz.kr/web/wmypage/myprofile/fundinglist/{userid}
# 입력값: userid
# 출력값: [켐페인id, 켐페인이름, 카테고리]
def get_user_fundinglist(userid):
    time.sleep(random.uniform(1,3))
    list_url = f"https://www.wadiz.kr/web/wmypage/myprofile/fundinglist/{userid}"
    funding_list = []
    res = requests.get(list_url, headers=headers).text
    soup = bs(res, 'html.parser')
    with requests.Session() as s:
        login_headers = {'authority':'www.wadiz.kr', 'method': 'POST', 'path': '/web/waccount/ajaxLoginProcess'
                   ,'scheme': 'https', 'accpet': 'application/json, text/javascript, */*; q=0.01',
                   'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        
        s.post("https://www.wadiz.kr/web/waccount/ajaxLoginProcess", headers=login_headers, data=user_data)
        res = s.get(list_url).text
        soup = bs(res, 'html.parser')
        card_list = soup.find_all('li', class_='all')
    for card in card_list:
        campaign_id = card.attrs['data-campaignid']
        name = card.find('h4').text
        category = card.find('span', class_='category1').text
        funding_list.append([campaign_id, name, category])
    return funding_list


# 함수이름: save_user_to_file
# 동작: 유저의 펀딩 리스트를 파일로 저장한다.(중복제거) 
# 입력값: userid, funding_list
# 출력값: 파일 수정 
def save_user_to_file(userid, funding_list):
    try:
        dfUser = pd.read_csv("users1.csv", names=['userid', 'funding_list'], header=None)
    except:
        dfUser = pd.DataFrame(columns=['userid', 'funding_list'])

    dfUser = dfUser.set_index('userid')

    if userid in dfUser.index:
        if len(dfUser.loc[userid]['funding_list']) != len(funding_list):
            dfUser.loc[userid]['funding_list'] = funding_list
        dfUser.to_csv("users1.csv", header=None)
    else:
        dfUser2 = pd.DataFrame({'userid':[userid], 'funding_list': [funding_list]}, columns=['userid', 'funding_list'])
        dfUser2 = dfUser2.set_index('userid')
        resultdf = pd.concat([dfUser, dfUser2])
        resultdf.to_csv("users1.csv", header=None)
        
# endYn = Y or ALL , order = recommend or recent or support or amount
endYn = 'Y'
order = 'recommend'
startNum  = 0

os.makedirs('result', exist_ok=True)
count = 1
for i in range(0, 100):
    time.sleep(random.uniform(1,3))
    finish_crawling_count = 48*i
    save_crawling_count = 48*(i+1)
    startNum = 48*i
    # 주소 : https://www.wadiz.kr/web/wreward/ajaxGetCardList?startNum={startNum}&limit=48&order={order}&keyword=&endYn={endYn}
    # 목록을 json형태로 받아온다.
    base_url = f"https://www.wadiz.kr/web/wreward/ajaxGetCardList?startNum={startNum}&limit=48&order={order}&keyword=&endYn={endYn}"
    print(finish_crawling_count)
    
    products_dict = requests.get(base_url, headers=headers)
    products_dict = products_dict.json()
    products = products_dict['data'] # 파이썬의 dictionary형태로 받아온다.
    
    print('There are %d Wadiz product available!' % len(products))
    print('Writing the data....')

    

    
   # count = finish_crawling_count
    for product in products:
        dfProduct = pd.DataFrame(columns=['id', 'name', 'category', 'makerName', 'summary', 'achievementRate', 
                               'totalAmount', 'totalSupporter', 'totalLike', 'rewardSatisfaction', 
                               'makerSatisfaction','detailUrl'])
        time.sleep(random.uniform(1,3))
        if True:
            detailUrl = "https://www.wadiz.kr/web/campaign/detail/" + str(product['campaignId'])
            id = product['campaignId']
            
            name = product['title']
            category = product['custValueCodeNm']
            makerName = product['nickName']
            achievementRate = product['achievementRate']
            totalAmount = product['totalBackedAmount']
            # 상품 상세정보
            summary, totalSupporter, totalLike = product_detail(id, detailUrl)
            # 상품 댓글 가져오기
            rewardSatisfaction, makerSatisfaction, comments = product_comment(id)
            
            campaigncomments = []
            # 응원댓글은 내용이 많아서 주석처리, 필요할경우만 사용 
            campaigncomments = product_comment2(id)

            participants = get_participants(id)

            for participant in participants:
                funding_list = get_user_fundinglist(participant[0])
                save_user_to_file(participant[0], funding_list)
            
                
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
            
        if comments != None:
            print(str(count) + ": " + name + ",  len_satiscomment: " + str(len(comments)) + ", len_campaigncomment: " + str(len(campaigncomments)))
        else:
            print(str(count) + ": " + name + ",  len_satiscomment: " + str(len(campaigncomments)))
            
        # 하나씩 csv파일로 저장.
        dfProduct.to_csv('wadiz0-100.csv', mode='a', header=False)
        count = count + 1
    
        

result = pd.read_csv('wadiz.csv')
print(result)
