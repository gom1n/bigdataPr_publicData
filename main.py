import requests
import pprint

#인증키 입력
encoding = 'wEOWhOEV95XFLOJ4fqYdWXwJMODD6Ze7R8%2FQDUZdmBrHnlVU8ER0P2YenWEkb4imfh7IvqniyzIfj%2BEZp%2BnG%2Fw%3D%3D'
decoding = 'wEOWhOEV95XFLOJ4fqYdWXwJMODD6Ze7R8/QDUZdmBrHnlVU8ER0P2YenWEkb4imfh7IvqniyzIfj+EZp+nG/w=='

#url 입력
url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
params ={'serviceKey' : decoding, 'pageNo' : '1', 'numOfRows' : '10', 'zcode' : '11' }

response = requests.get(url, params=params)
# xml 내용
content = response.text
# 깔끔한 출력 위한 코드
pp = pprint.PrettyPrinter(indent=4)
# print(pp.pprint(content))

## 각 컬럼 값 ## (포털 문서에서 꼭 확인하세요)
"""
결과코드	resultCode
결과메시지	resultMsg
전체 결과 수	totalCount
페이지 번호	pageNo
한 페이지 결과 수	numOfRows
충전소명	statNm
충전소ID	statId
충전기ID	chgerId
충전기타입	chgerType
소재지 도로명 주소	addr
위도	lat
경도	lng
이용가능시간	useTime
기관ID	busiId
운영기관명	busiNm
관리업체 전화번호	busiCall
충전기상태	stat
상태갱신일시	statUpdDt
충전기용량	powerType
지역코드	zcode
주차료무료 여부	parkingFree
충전소 안내	note
"""

### xml을 DataFrame으로 변환하기 ###
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote

#bs4 사용하여 item 태그 분리

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('item')

# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]

#xml값 DataFrame으로 만들기
# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)
corona_df = pd.DataFrame(row_list, columns=name_list)

print(corona_df)