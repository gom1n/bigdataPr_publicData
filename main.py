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
print(pp.pprint(content))