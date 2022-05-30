import requests
import pprint

# 인증키 입력
encoding = 'wEOWhOEV95XFLOJ4fqYdWXwJMODD6Ze7R8%2FQDUZdmBrHnlVU8ER0P2YenWEkb4imfh7IvqniyzIfj%2BEZp%2BnG%2Fw%3D%3D'
decoding = 'wEOWhOEV95XFLOJ4fqYdWXwJMODD6Ze7R8/QDUZdmBrHnlVU8ER0P2YenWEkb4imfh7IvqniyzIfj+EZp+nG/w=='

# url 입력
url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
params = {'serviceKey': decoding, 'pageNo': '1', 'numOfRows': '9999'}

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
elif platform.system() == 'Darwin':  # Mac
    plt.rc('font', family='AppleGothic')
else:  # linux
    plt.rc('font', family='NanumGothic')

plt.rc('font', size=20)        # 기본 폰트 크기
plt.rc('axes', labelsize=20)   # x,y축 label 폰트 크기
plt.rc('xtick', labelsize=6)  # x축 눈금 폰트 크기
plt.rc('ytick', labelsize=7)  # y축 눈금 폰트 크기
plt.rc('legend', fontsize=20)  # 범례 폰트 크기
plt.rc('figure', titlesize=50) # figure title 폰트 크기

zcode_arr = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
df_count = only_zcode.to_numpy()


# 숫자 label 추가
def add_value_label(x_list, y_list):
    for i in range(1, len(x_list) + 1):
        plt.text(i, y_list[i-1], y_list[i-1], fontsize=5, color='purple', horizontalalignment='center',
                 verticalalignment='bottom')

plt.title('지역별 전기자동차 충전소 현황')
# x축 라벨 설정
plt.xlabel('지역')
# x축 라벨 설정
plt.ylabel('충전소 개수')
# 막대 그래프(x, y)
plt.bar(zcode_arr, df_count, color='purple', alpha=0.3)
add_value_label(zcode_arr, df_count)
# 그래프 출력
plt.show()

## 지도 출력
# x좌표(위도),y좌표(경도) 리스트로 만들기
x = []
y = []
name = []
state = []
for i in range(len(station_df['lat'])):
    if station_df['lat'][i] == 0.0 or station_df['lat'][i] == 0.0:
        pass
    else:
        name.append(station_df['statNm'][i])
        x.append(station_df['lat'][i])
        y.append(station_df['lng'][i])
        state.append(station_df['stat'][i])

#지도 생성
import folium

m = folium.Map(location=[36.0,126.986],zoom_start=7)

for i in range(len(x)):
    folium.Circle(
        location = [x[i], y[i]],
        tooltip = name[i],
        radius = 200,
        color='violet'
    ).add_to(m)

m.save('station.html')

def state_color(state_list):
    if state_list == '2':
        return 'blue'
    if state_list == '3':
        return 'yellow'
    else:
        return 'red'

m = folium.Map(location=[36.0,126.986],zoom_start=7)
for i in range(len(x)):
    folium.Circle(
        location = [x[i], y[i]],
        tooltip = name[i],
        radius = 200,
        color=state_color(state[i])
    ).add_to(m)

m.save('station_state.html')