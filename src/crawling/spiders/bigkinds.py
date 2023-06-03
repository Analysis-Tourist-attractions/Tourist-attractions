# !pip install selenium
# !pip install webdriver_manager

# 0. 필요한 모델 Import

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.keys import Keys
import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# func 1 : Setup - 최초 검색어, 검색 날짜 설정


def setup():
    global ask_place, start_date, ending_date, login_id, login_pw
    ask_place = input("1. 지명 입력")
    ask_start_date = input("2. 기사를 검색하고자하는 시작범위('~년 ~월) \n (예- 2017년3월이면 '201703'")
    login_id = input("3.id_입력")
    login_pw = input("4.pw 입력")
    start_date = dt.datetime.strptime(ask_start_date, "%Y%m")
    ending_date = start_date + relativedelta(months=3)


# func 2 : get_chrome_driver - 크롬드라이버 가져오기


def get_chrome_driver():
    # 1.브라우저 옵션 세팅
    chrome_options = webdriver.ChromeOptions()
    # 2.driver 생성
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver


# func 3 : run_driver - 크롬드라이버 실행
def rundriver():
    # 크롬드라이버 실행
    driver = get_chrome_driver()
    driver.get("https://www.bigkinds.or.kr/")


def login():
    # 로그인
    time.sleep(5)
    driver.set_window_size(1800, 800)
    login = driver.find_element(
        By.CSS_SELECTOR,
        "#header > div.hd-top > div > div.login-area > button.btn-login.login-modal-btn.login-area-before",
    )
    login.click()

    # id 입력
    bigkinds_login = driver.find_element(By.CSS_SELECTOR, "#login-user-id")

    bigkinds_login.send_keys(f"{login_id}")

    # pw 입력
    bigkinds_pw = driver.find_element(By.CSS_SELECTOR, "#login-user-password")
    bigkinds_pw.send_keys(f"{login_pw}")

    # 로그인버튼 클릭
    driver.find_element(By.CSS_SELECTOR, "#login-btn").click()


def search():
    query_elem = driver.find_element(By.CSS_SELECTOR, "#total-search-key")
    query_elem.click()
    query_elem.send_keys(f"{ask_place}")

    time.sleep(0.5)
    # 검색 버튼 누르기
    driver.find_element(
        By.CSS_SELECTOR, "#news-search-form > div > div.hd-srch.v2 > button"
    ).click()
    time.sleep(0.5)
    # 기간 버튼
    date_btn = driver.find_element(
        By.CSS_SELECTOR,
        "#news-search-form > div > div.hd-srch.v2 > div.srch-detail.v2 > div > div.tab-btn-wp1 > div.tab-btn-inner.tab1 > a",
    )

    date_btn.click()
    time.sleep(0.5)
    # 시작 날짜 입력
    begin_date = driver.find_element(By.CSS_SELECTOR, "#search-begin-date")
    begin_date.click()
    begin_date.send_keys(Keys.CONTROL + "A")
    begin_date.send_keys(Keys.BACKSPACE)
    begin_date.send_keys(str(start_date).split(" ")[0])
    time.sleep(0.5)
    # 끝날짜 입력
    end_date = driver.find_element(By.CSS_SELECTOR, "#search-end-date")
    end_date.click()
    end_date.send_keys(Keys.CONTROL + "A")
    end_date.send_keys(Keys.BACKSPACE)
    end_date.send_keys(str(ending_date).split(" ")[0])
    # 스크롤
    #  자바스크립트를 문자열로 작성해서 실행
    driver.execute_script("window.scrollTo(50, 600)")

    # 기사클릭
    search_article = driver.find_element(
        By.CSS_SELECTOR,
        "#search-foot-div > div.foot-btn > button.btn.btn-search.news-search-btn.news-report-search-btn",
    )
    search_article.click()


# 뉴스기사 다운로드
def download():
    # 검색결과 탭 닫기
    driver.find_element(By.CSS_SELECTOR, "#collapse-step-2").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#collapse-step-3").click()
    time.sleep(2)
    # 다운로드
    driver.find_element(
        By.CSS_SELECTOR, "#analytics-data-download > div.btm-btn-wrp > button"
    ).click()


setup()
rundriver()
login()
search()
download()
