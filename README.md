# 🖥️ 국내 주요 관광지 대비 특이 지역 선정 및 분석

- 최근 국내 여행의 수요가 증가하여 기존 국내 여행 수요 지역에 대한 변화가 존재 했을 것이라는 기대와 달리 데이터 분석 결과 기존의 인기 관광 지역의 언급량 변화가 없음을 확인 후 그렇다면 일반적인 관광지역과 달리 특이성을 갖는 지역에 대해 분석

- 6명의 팀원들이 각자 데이터수집과 분석, 모델링, DB구축 및 자연어 처리 등의 역할을 나누어 수행
 
- 🕰️ 프로젝트 기간 : 2023-05-03 ~ 2023-05-24

## Table of Contents

### Architecture
<img width="1200" alt="image" src="https://github.com/Analysis-Tourist-attractions/Tourist-attractions/assets/121608383/e67e2432-fc52-46c8-9352-e2f6a8415dca">

### Library 
```
python : 3.9.7
sklearn : 1.0.1
lightgbm : 3.1.1
tensorflow : 2.7
pandas : 1.3.5
numpy : 1.21.4
matplotlib.pyplot : 3.5.0
```

### DataFrame
- 독립변수 : 거리별 방문자 수 / 내비게이션 검색량
- 종속변수 : 방문자 소비액
<img width="1200" alt="image" src="https://github.com/Analysis-Tourist-attractions/Tourist-attractions/assets/121608383/9bb9fad2-e33c-4468-bd90-c9ea54fcc535">

### Project Process
- 데이터 수집
    
    거리별 방문자 수 , 내비 검색 건수, 지출액, 블로그 크롤링
    (한국관광 데이터랩,  네이버 블로그, 네이버뉴스, 빅카인즈)
    
- 전처리
    
    - Pandas, MinMax Scalar, One-Hot encoding, Okt, Mecab
    
    - 머신러닝 Scikit-Learning
        
      - TF-IDF vectorizer, Countervectorizer, K-means, LDA
        
    - 딥러닝 Tensorflow
      - Tokenizer
        
    - MySQL을 활용하여 AWS Cloud에 저장
      - 팀 프로젝트로 완성한 서비스를 서버로 제공할 때 Amazon EC2의 웹 서비스 인터페이스를 사용하여 인스턴스(서버)를 쉽고 간단하게 구현할 수 있으며, 높은 안정성으로 유연하게 서비스 관리를 할 수 있기 때문에 aws를 선택
        

- EDA 및 데이터 시각화
    
   - Matplotlib, Seaborn
    
- 예측모델을 통한 지역 예측

<img width="500" height="500" alt="image" src="https://github.com/Analysis-Tourist-attractions/Tourist-attractions/assets/121608383/a5ba5f0e-573b-435c-bbc6-12cd555cd7b9">

<img width="500" height="500" alt="image" src="https://github.com/Analysis-Tourist-attractions/Tourist-attractions/assets/121608383/628868b2-5a1d-4c51-a752-5f03c63de2e9">

- K-means 클러스터링 결과

<img width="1324" alt="image" src="https://github.com/Analysis-Tourist-attractions/Tourist-attractions/assets/121608383/860f7e48-aaa6-4ae5-bd2c-2d395806533f">


### Analysis
- 정량적 분석
  - 지역별 방문자 수, 검색량 증가 등의 지표를 분석하여 트렌드 도출

- 정성적 분석
  - 여행자 리뷰, 소셜 미디어 게시물 등을 분석하여 인기 증가의 원인과 관련된 의견 수집

- 머신러닝
  - LightGBM(250개의 지역의 상위 10위 지역 추출) : 모델의 일반화를 보여주는 잔차를 통해 이상 지역 탐지 

- 군집화, 토픽모델링
  - K-means, LDA
 
### Module
  - 구성 : sql.py, encoding.py, XGBR.py, LSTM_Module.py
  - 순서 : sql.py -> encoding.py -> XGBR.py or LSTM_Module.py
      - sql.py : SQLite로 DB 파일 만들고 데이터를 저장한 후 데이터테이블을 파이썬에 재추출
      - encoding.py : DB에서 추출한 데이터를 분석에 적합하도록 조작
      - LSTM_Module.py : LSTM 시계열 예측 분석(구글 코랩에서 분석되도록 세팅)
      - LGBM
      - LDA 단어 빈도수를 기반하여 DTM 단어 행렬을 생성
          - 토큰화 한 단어들의 counterverctorizer 사용하여 벡터화
       
### Prerequisite 
```
from konlpy.tag import Okt
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
```

### 의의 및 한계

의의

<img width="1268" alt="image" src="https://github.com/Analysis-Tourist-attractions/Tourist-attractions/assets/121608383/14611cea-c0eb-4126-9904-d6438f2500f8">

- 기존의 인기지역과 대비되는 특이 지역들은 지역적 특색 부족으로 인해 방문객의 유입이 일정한 패턴을 띄지 않는다는 결과를 도출할 수 있음 따라서 이러한 특이 지역들도 인기 관광 지역처럼 성장하기 위하여 유휴 공간 활성화, 지역 고유 문화 컨텐츠 구축 등의 방법을 활용하는 것을 제안
    - 언제 어디서든 찾기 쉬운 지역 관광 정보 제공
    - 유휴 공간의 활성화
    - 지역 고유의 문화 콘텐츠 구축
    - 잠재 관광수요 촉진을 위한 부가혜택
 
한계
- 국내 여행 행태가 일반적이지 않은 지역을 발견하고 싶었음
  - 매출액, 네비게이션 검색량, 방문자 수의 일반화된 관계가 존재할 것이라고 가정하였음
  - 일반적이지 않은 지역을 발견하고자 함.
  - 매출액을 종속변수로 설정하고 예측된 매출액과의 잔차를 확인하여 관계를 파악하고자 함.
  - 생각보다 극명한 차이가 존재하는 지역을 발견하지는 못했음. 
  - Q. 가설 검정 결과가 예상과 다를 때 어떻게 대처했어야 했을까?
  - Q. 어떤 피처를 포함하면 더 유의미한 결과를 얻을 수 있었을까?

- 모델 선정
  - 선형모델 → 기본 가정을 만족하지 않음
  - 머신러닝모델 → 트리모델을 사용
      - Linear regression → 트리모델보다 큰 MSE

- 모델 성능 평가 지표 선택
  - test set이 존재하지 않을 때, 예측 모델의 성능평가 지표 선정 기준은 무엇인가?

- 잔차그래프 확인

  - 선택한 모델에 따라 발생한 잔차를 기준으로 일반적이지 않은 지역을 선정하고자 함. 그러나 어떻게 그래프를 해석해야 하는지에 대한 문제가 발생

  - 배운점 : 비즈니스 로직에 따라 해석 방법이 달라진다!
  
    1) 전체 기간에 대하여 잔차의 평균을 확인한다
    
    2) 잔차의 진폭이 큰 지역을 선택한다.
    
    3) 0을 기준으로 잔차의 진동이 큰 지역을 선택한다
    
      - 잔차의 진동이 큰 지역을 선택함. 모델이 가장 일반화하지 못한 지역이라고 판단함
      
      - 잔차의 진동을  x축과 잔차그래프의 면적으로 파악함.
      
      - Q. 이 로직이 정말 논리적인 로직이었을까? 더 최선의 선택은 없었을까?

- 선정한 지역에 대하여 텍스트 마이닝을 통해 특성을 파악하고자 함.
    - 네이버 뉴스
    - 다음 뉴스
    - 빅카인즈
    - 블로그
      
    - 문제점 :
        - 키워드 선정 - 원하는 문서를 얻기 위한 키워드 선정에 문제가 있었음. 지역에 관련된 전반적인 문서를 얻고자 했으므로 “지역명”를 키워드로 사용함
        - 어떤 단계에서 LDA를 진행하는가?
            1. 전체 문서에 대한 LDA를 진행하고 비슷한 내용으로 클러스터링
                
                - 키워드가 포괄적이라서 너무 다양한한 토픽이 추출됨. 프로젝트 방향과 맞지 않다고 판단하여 키워드를 수정하여 다시 추출하기로 결정:  “지역명+가볼만한 곳”
                - 여전히 토픽의 범위가 너무 넓음
                - 여행과 관련이 없는 문서를 먼저 선별하는 것이 필요하다고 판단함
                - “여행,관광,휴가,호텔,볼거리,숙소,맛집”이 포함된 문서만 선별하여 사용
                
            2. 전체 문서를 먼저 클러스터링하고 각 군집에 대하여 LDA
                
                - case1) 예상보다 돈을 많이 번 지역(상위5), 못 번 지역(하위5) 각각 LDA해서 토픽 추출
                - case2) 전체 문서를 클러스터링해서 전체 지역을 3~4개 카테고리로 분류

 
