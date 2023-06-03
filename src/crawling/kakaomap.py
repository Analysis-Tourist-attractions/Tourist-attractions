# 기본 실행 준비

# 1. 셀레니움
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 2. 시간 제어
import time
from time import sleep

# 3. 키보드 제어
from selenium.webdriver.common.keys import Keys

# 4. 데이터 저장
import pandas as pd

# 5. 예외처리 에러 임포트
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    ElementNotInteractableException,
    NoSuchWindowException,
)


def set_region():
    global region_list
    region_list = [
        "광주 광산",
        "대구 달성",
        "성북구",
        "성동구",
        "인천 서구",
        "울산 중구",
        "동대문구",
        "부천시",
        "부산진구",
        "관악구",
        "김해시",
    ]


def get_chrome_driver():
    # 1.브라우저 옵션 세팅
    chrome_options = webdriver.ChromeOptions()
    # 1-2. 안보이게
    chrome_options.headless = True
    # 2.driver 생성
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    return driver


set_region()
for region in region_list:
    region_data = {}
    place_data = []
    place_type_data = []
    review_data = []
    # 접속

    driver = get_chrome_driver()
    url = "https://map.kakao.com/"
    driver.get(url)
    time.sleep(0.2)

    # 검색어 입력
    search_bar = driver.find_element(By.CSS_SELECTOR, "#search\.keyword\.query")
    time.sleep(0.2)
    search_bar.send_keys(f"{region}")

    # 엔터
    driver.find_element(By.CSS_SELECTOR, "#search\.keyword\.submit").send_keys(
        Keys.ENTER
    )

    time.sleep(3)

    # ActionChains모듈 가져오기 - 스크롤 통제
    # 스크롤 다운 하지 않아도 알아서 클릭 가능
    from selenium.webdriver import ActionChains

    action = ActionChains(driver)

    try:
        # 더보기 셀렉터
        More_WebElement = driver.find_element(
            By.CSS_SELECTOR, "#info\.search\.place\.more"
        )

        # 더보기 클릭
        action.double_click(More_WebElement).perform()
    except ElementNotInteractableException:
        pass
    time.sleep(3)

    # -- !! 데이터를 뽑고 싶은 페이지 = range(n)

    for change_page in range(2):
        # find_elements는 리스트로 저장되니까 이것을 변수에 담기
        # 지명
        name_list = driver.find_elements(By.CSS_SELECTOR, ".link_name")
        review_num_list = driver.find_elements(By.CSS_SELECTOR, ".numberofscore")

        # 지명 저장
        for name in name_list:
            place_data.append(name.text)

        for i in range(len(review_num_list)):
            # 리뷰 데이터에 저장
            old_review_data = []
            review_data = []

            # 총 리뷰수 = review_num
            try:
                review_num = int(review_num_list[i].text.replace("건", ""))
            except ValueError as e:
                review_num = 0
            # i번째 장소 선택
            time.sleep(0.5)
            try:
                # 접속 ~
                driver.find_element(
                    By.CSS_SELECTOR,
                    f"#info\.search\.place\.list > li:nth-child({i+1}) > div.rating.clickArea > span.score > a",
                ).send_keys(Keys.ENTER)

                # 컨트롤을 크롬의 2번째 탭으로 전환
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)

            # 리뷰페이지가 없는 곳
            except ElementNotInteractableException:
                print(f"{change_page*len(review_num_list)+i+1}번째 데이터는 리뷰 제공을 하지 않습니다.")

            # 장소 유형 추출
            try:
                loc_type = driver.find_element(
                    By.CSS_SELECTOR, "span.txt_location"
                ).text

            # 리뷰페이지가 없는 곳
            except ElementNotInteractableException:
                loc_type = ""
            except NoSuchElementException:
                loc_type = ""
            # 더보기 클릭수 = 총 리뷰수-3//5+1 (더보기 안해도 있는 리뷰 세개 제거, 더보기 할 때마다 5개씩 +1은 반올림)
            if (review_num - 3) % 5 == 0:
                if review_num > 3:
                    # 반복으로 더보기 클릭
                    for click_num in range((review_num - 3) // 5):
                        More_Text_WebElement = driver.find_element(
                            By.CSS_SELECTOR,
                            "#mArticle > div.cont_evaluation > div.evaluation_review > a > span.txt_more",
                        )
                        time.sleep(0.5)

                        More_Text_WebElement.click()
                        time.sleep(0.5)
                        # 클릭수가 최대일때
                        if click_num == (review_num - 3) // 5 - 1:
                            # 리뷰 전체 추출
                            review_list = driver.find_elements(
                                By.CSS_SELECTOR, ".txt_comment"
                            )
                            # 데이터에 저장
                            for review in review_list:
                                old_review_data.append(review.text)
                            # 창 닫기
                            driver.close()

                else:
                    # 리뷰 전체 추출
                    review_list = driver.find_elements(By.CSS_SELECTOR, ".txt_comment")
                    # 데이터에 저장
                    for review in review_list:
                        old_review_data.append(review.text)
                    # 창 닫기
                    driver.close()

            else:
                if review_num > 3:
                    for click_num in range((review_num - 3) // 5 + 1):
                        More_Text_WebElement = driver.find_element(
                            By.CSS_SELECTOR,
                            "#mArticle > div.cont_evaluation > div.evaluation_review > a > span.txt_more",
                        )
                        time.sleep(0.5)
                        # 반복으로 더보기 클릭
                        More_Text_WebElement.click()
                        time.sleep(0.5)

                        # 클릭수가 최대일때
                        if click_num == (review_num - 3) // 5:
                            # 리뷰 전체 추출
                            review_list = driver.find_elements(
                                By.CSS_SELECTOR, ".txt_comment"
                            )
                            # 데이터에 저장
                            for review in review_list:
                                old_review_data.append(review.text)
                            # 창 닫기
                            driver.close()

                # 리뷰수가 0일때
                elif review_num == 0:
                    review_list = [""]
                    old_review_data.append(review_list[0])

                    try:
                        check = driver.find_element(
                            By.CSS_SELECTOR, "#mArticle > div.cont_review > div > h3"
                        )
                        print(
                            f"{change_page*len(review_num_list)+i+1}번째 데이터는 리뷰수가 0건입니다."
                        )
                        driver.close()
                    except NoSuchElementException:
                        print("리뷰 페이지에 접속할 수 없습니다.")
                        pass
                else:
                    review_list = driver.find_elements(By.CSS_SELECTOR, ".txt_comment")
                    # 데이터에 저장
                    for review in review_list:
                        old_review_data.append(review.text)
                    # 창 닫기
                    driver.close()

            # 데이터 정제 1. 빈 데이터 제거
            old_review_data = list(filter(None, old_review_data))

            # 데이터 정제 2. \n처리
            for old_review in old_review_data:
                review = old_review.replace("\n", ". ")
                review_data.append(review)

            # 데이터 정제 3. 하나로 합치기
            review_data = ["".join(review_data)]
            print(
                f"{change_page*len(review_num_list)+i+1}번째 장소({place_data[change_page*len(review_num_list)+i]})리뷰 저장완료"
            )
            time.sleep(1)

            # 데이터 정제 4. 저장
            region_data[
                f"{place_data[change_page*len(review_num_list)+i]}[{loc_type}]"
            ] = review_data
            print(f"{change_page*len(review_num_list)+i+1}번째 데이터 저장완료")

            # 다시 '카카오맵' 페이지에서 컨트롤하도록 실행
            driver.switch_to.window(driver.window_handles[0])

        # 다음페이지 넘어가기
        try:
            driver.find_element(
                By.CSS_SELECTOR, f"#info\.search\.page\.no{change_page+2}"
            ).click()
            print(f"{change_page+2}페이지로 이동")
            time.sleep(2)
        # 다음페이지 없으면 건너뛰기
        except ElementNotInteractableException:
            print(f"다음 페이지가 없습니다. 앞으로 {4-change_page}회 만큼 반복하고 종료합니다.")
            pass
    print(f"데이터 총{len(region_data)}개 수집완료. 파일을 저장하고 마무리합니다.")
    time.sleep(2)

    # 완성된 데이터 DataFrame으로 저장
    df = pd.DataFrame(list(region_data.items()), columns=["장소명", "리뷰"])
    df.to_csv(f"{region}.csv", index="False")
    # 미리보기 파일
    df.to_excel(f"{region}.xlsx")
    print(f"'{region}' 지역 데이터 다운로드 완료.")
# 전체종료
for i in range(3):
    print(f"{3-i}초 후에 종료.")
    time.sleep(1)
driver.quit()
