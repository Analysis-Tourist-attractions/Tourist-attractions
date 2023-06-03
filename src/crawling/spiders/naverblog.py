from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd
import re
import os
import sys
import urllib.request
import pandas as pd
import json

# !pip install selenium
# !pip install newspaper3k
# !pip install webdriver_manager

# naver 블로그 검색 url
NAVER_WEB_SEARCH_URL = "https://openapi.naver.com/v1/search/blog.json?query={}&sort=date"

# 크롬드라이버 설정
def get_chrome_driver():
    # 1.브라우저 옵션 세팅
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    options.addArguments("lang=ko")
    
    # 2.driver 생성
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()),
        options = chrome_options
                    )
    return driver

# 특정 단어 검색 및 데이터프레임 형성

############################### STEP 1

# 네이버 블로그 url 추출
def naver_blog_urls(items):
    global CLIENT_ID,NAVER_API_KEY
    search_li = items # @@@@ 여기에 원하는 검색어 넣기 @@@@
    result_urls = [[] for i in range(len(search_li))]

    for i in search_li:
        
        for start_num in range(1,1000,100):
            try:
                client_id = CLIENT_ID
                client_secret = NAVER_API_KEY
                encText = urllib.parse.quote(i) # json 결과
                url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=100&sort=date&start={}".format(start_num)# JSON 결과
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",client_id)
                request.add_header("X-Naver-Client-Secret",client_secret)
                response = urllib.request.urlopen(request) 
                rescode = response.getcode()

                if(rescode==200):
                    response_body = json.load(response) # 딕셔너리 형태
                    if start_num==1 and i == search_li[0]:
                        df_search = pd.DataFrame(response_body)
                    df_search_new = pd.DataFrame(response_body) # 데이터프레임
                    df_search=pd.concat([df_search,df_search_new],axis=0,ignore_index=True)
                else:
                    print("Error Code:" + rescode)
                for p in range(len(response_body['items'])):
                    result_urls[search_li.index(i)].append(response_body['items'][p]['link'])
            except:
                pass
    return search_li,df_search, result_urls
####################

# link별로 본문내용 추출
def blog_contents(search_li, result_urls):
    contents = [[] for i in range(len(search_li))]
    driver=webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(2)
    
    for k in result_urls:
        for i in k:
            driver.get(i)
            time.sleep(1)
            try:
                #블로그 안 본문이 있는 iframe에 접근하기(pc버전)
                driver.switch_to.frame("mainFrame")
                #모바일 버전으로 변경할것
                #본문 내용 크롤링하기
                try:
                    a = driver.find_element(By.CSS_SELECTOR,'div.se-main-container').text
                    contents[result_urls.index(k)].append(a.replace("\n",'').replace('/','').strip())
                # NoSuchElement 오류시 예외처리(구버전 블로그에 적용)
            #     except NoSuchElementException:
                except:
                    pass
                #print(본문: \n', a)
            except:
                pass
    driver.quit() #창닫기
    print("<<본문 크롤링이 완료되었습니다.>>")
    return contents
#####################
# 블로그 본문 파일로 저장
def blog_save_file(search_li,contents):
    for i in range(len(search_li)):
        news_df = pd.DataFrame({'search_li': contents[i]})
        news_df = news_df.drop_duplicates()
        #CSV로 저장하기
        news_df.to_csv('NaverBlogs_%s.csv' % search_li[i].replace('"',''), index=False, encoding='utf-8-sig')

        
################
# 최종 함수
def naver_blog_search():
    global CLIENT_ID,NAVER_API_KEY
    items = list(input("검색할 내용 : ").split(','))
    search_li, df_search, result_urls = naver_blog_urls(items)
    contents = blog_contents(search_li, result_urls)
    blog_save_file((search_li,contents))
    
CLIENT_ID= ''
NAVER_API_KEY=''
naver_blog_search()