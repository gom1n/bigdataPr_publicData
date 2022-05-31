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

