import requests
import pprint

# 인증키 입력
encoding = 'wEOWhOEV95XFLOJ4fqYdWXwJMODD6Ze7R8%2FQDUZdmBrHnlVU8ER0P2YenWEkb4imfh7IvqniyzIfj%2BEZp%2BnG%2Fw%3D%3D'
decoding = 'wEOWhOEV95XFLOJ4fqYdWXwJMODD6Ze7R8/QDUZdmBrHnlVU8ER0P2YenWEkb4imfh7IvqniyzIfj+EZp+nG/w=='

# url 입력
url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
params = {'serviceKey': decoding, 'pageNo' : '1', 'numOfRows' : '9999'}

response = requests.get(url, params=params)
# xml 내용
content = response.text
# 깔끔한 출력 위한 코드
pp = pprint.PrettyPrinter(indent=4)
# print(pp.pprint(content))

### xml을 DataFrame으로 변환하기 ###
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote

# bs4 사용하여 item 태그 분리

xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
rows = xml_obj.findAll('item')

# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = []  # 행값
name_list = []  # 열이름값
value_list = []  # 데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    # 첫째 행 데이터 수집
    for j in range(0, len(columns)):
        if i == 0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list = []

# xml값 DataFrame으로 만들기
# row 생략 없이 출력
# pd.set_option('display.max_rows', None)
# # col 생략 없이 출력
# pd.set_option('display.max_columns', None)
station_df = pd.DataFrame(row_list, columns=name_list)

loc_df = station_df.groupby('zcode')
only_zcode = loc_df.size()
print(only_zcode)

import matplotlib.pyplot as plt
import platform

# Window
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
else: #linux
    plt.rc('font', family='NanumGothic')

zcode_arr = ['11', '26', '27', '28', '29', '30', '31', '36', '41', '42', '43', '44', '45', '46', '47', '48', '50']
df_count = only_zcode.to_numpy()

# 숫자 labe 추가
def add_value_label(x_list,y_list):
    for i in range(1, len(x_list)+1):
        plt.text(i,y_list[i-1],y_list[i-1], fontsize=5, color='blue', horizontalalignment='left', verticalalignment='bottom')


plt.title('지역별 전기자동차 충전소 현황')
# x축 라벨 설정
plt.xlabel('지역')
# x축 라벨 설정
plt.ylabel('충전소 개수')
# 막대 그래프(x, y)
plt.bar(zcode_arr, df_count)
add_value_label(zcode_arr,df_count)
# 그래프 출력
plt.show()