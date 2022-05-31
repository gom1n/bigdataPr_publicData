import pandas as pd
import numpy as np

## 데이터 불러오기
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
data = pd.read_csv('22.2월 자치구별연료별차종별용도별.csv')

data = data.drop([0, 1, 2, 3, 4, 5, 6, 7])
# print(data)

## 지역구 이름 배열 구하기
location_array = []
for i in range(len(data)):
    if i > 7:
        location_array.append(data['Unnamed: 0'][i])

arr = np.array(location_array, dtype='str')
location_d = []
for i in range(len(arr)):
    if arr[i] != 'nan':
        location_d.append(arr[i])

# 중복 제거
location = []
for v in location_d:
    if v not in location:
        location.append(v)
print(location)

n = len(location)
count = 0
elec_count = [0 for i in range(n)]
category = ['전기', '하이브리드(LPG+전기)', '하이브리드(경유+전기)', '하이브리드(휘발유+전기)']
for i in range(len(data)):
    if i > 8:
        val = data['Unnamed: 3'][i]
        if val in category:
            count2 = count // 2
            num = data['Unnamed: 15'][i]
            elec_count[count2] = elec_count[count2] + int(num)
        if val == 'CNG':
            count = count + 1

print(elec_count)

## 막대 그래프
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
plt.rc('axes', labelsize=10)   # x,y축 label 폰트 크기
plt.rc('xtick', labelsize=6)  # x축 눈금 폰트 크기
plt.rc('ytick', labelsize=7)  # y축 눈금 폰트 크기
plt.rc('legend', fontsize=20)  # 범례 폰트 크기
plt.rc('figure', titlesize=50) # figure title 폰트 크기

# 숫자 label 추가
def add_value_label(x_list, y_list):
    for i in range(1, len(x_list) + 1):
        plt.text(i, y_list[i-1], y_list[i-1], fontsize=15, color='purple', horizontalalignment='center',
                 verticalalignment='bottom')

plt.title('자치구별 전기자동차 등록 현황')
# x축 라벨 설정
plt.xlabel('개수')
# x축 라벨 설정
plt.ylabel('자치구')
# 막대 그래프(x, y)
plt.barh(location, elec_count, color='purple', alpha=0.3)
add_value_label(location, elec_count)
# 그래프 출력
plt.show()


## 지도 생성
import folium

loc_df = pd.DataFrame({ 'LOCATION':location, 'COUNT':elec_count })
print(loc_df)

m = folium.Map(location=[37.562225, 126.978555], tiles="OpenStreetMap", zoom_start=11)
state_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
m.choropleth(
    geo_data=state_geo,
    name='인당소득',
    data=loc_df,
    columns=['LOCATION', 'COUNT'],
    key_on='feature.properties.name',
    fill_color='Blues',
    fill_opacity=0.7,
    line_opacity=0.3,
    color = 'gray',
    legend_name = 'income'
)
m.save('car.html')