import requests
import json
import speech_recognition as sr
import time
import datetime
from selenium import webdriver
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import pandas as pd
from datetime import datetime,timedelta
import xmltodict # 결과가 xml 형식으로 반환된다. 이것을 dict 로 바꿔주는 라이브러리다

def weather():
    #API키를 지정한다. 여러분들의 API키를 사용
    apikey="bec80734c13b7e66e1edfd921d02b6f4"

    city_list = ["Ulsan,KR"]

    #API 지정
    api="http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

    # 켈빈 온도를 섭씨 온도로 변환하는 함수
    k2C = lambda k: k - 273.15

    #각 도시의 정보를 추출하기
    for name in city_list:
        
        #API의 URL 구성하기
        url = api.format(city=name, key=apikey)

        #API요처을 보내 날씨 정보를 가져오기
        res = requests.get(url)

        #JSON형식의 데이터를 파이썬형으로 변환한다.
        data = json.loads(res.text)

        #결과를 출력하기
        print("** 도시 = ", data["name"])
        print("| 날씨 = ", data["weather"][0]["description"])
        print("| 최저기온 = ", k2C(data["main"]["temp_min"]))
        print("| 최고기온 = ", k2C(data["main"]["temp_max"]))
        print("| 습도 = ", data["main"]["humidity"])
        print("| 기압 = ", data["main"]["pressure"])
        print("| 풍향 = ", data["wind"]["deg"])
        print("| 풍속 = ", data["wind"]["speed"])
        print(" ")

def music():
    # Chrome WebDriver를 이용해 Chrome을 실행한다.
    driver = webdriver.Chrome("./chromedriver")
 
 
# # 오늘 날짜를 계산한다 
#     d = str(datetime.datetime.now().day)  
#     m = str(datetime.datetime.now().month)
    
#     query = m + '월' + d + '일 멜론'
#     query2 = m + '월 ' + d + '일'
    temp = '조용히 혼자 있고 싶을 때 듣는 감성음악'
 
    driver.get("https://www.youtube.com/results?search_query=" + temp)
    time.sleep(1)
 

    # 검색된 내용 중 링크 텍스트에 "{month}월 {day}일" 이 포함된 것을 찾는다.
    continue_link = driver.find_element_by_partial_link_text(temp)
 
    # 해당 링크를 클릭한다.
    continue_link.click()

    time.sleep(200)

def covid():
        # 어제 날짜와 오늘날짜를 구하기 위해서  datetime과 timedelta를 사용
    yester = datetime.today() - timedelta(1)
    yseter =  yester.strftime("%Y%m%d")
    now_today = datetime.today().strftime("%Y%m%d")

    my_api_key = 'gT9WUcrDp1uBxyf2XTG2Mb3B3luRl1VDTRm5fNT3caEhhw6Y1XMl5n6nJcWoi9dk2rxWAQuSn2N/eSmoIjWjhQ=='

    # 서비스 url 주소
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'

    # 서비스에 필요한 파라미터 모음
    queryParams = '?' + \
    'ServiceKey=' + '{}'.format(my_api_key) + \
    '&pageNo='+ '1' + \
    '&numOfRows='+ '999' + \
    '&startCreateDt={}&endCreateDt={}'.format(yseter,now_today)

    #서비스url에 필요한 파라미터들을 붙여서 응답결과를 얻음.
    result = requests.get(url + queryParams)

    # 응답결과 파싱하기. ( 사용자가 원하는 형태로 변경)
    # 응답 key 값이 영문화 되어 식별이 어려워 openAPI 문서를 참고하여
    # replayce 를 통해 결과를 한글화 했다.

    result = result.content 
    jsonString = json.dumps(xmltodict.parse(result), indent = 4)
    jsonString = jsonString.replace('resultCode', '결과코드').replace('resultMsg', '결과메세지').replace('numOfRows', '한 페이지 결과 수').replace('pageNo', '페이지 수').replace('totalCount', '전체 결과 수').replace('seq', '게시글번호(감염현황 고유값)').replace('stateDt', '기준일').replace('stateTime', '기준시간').replace('decideCnt', '확진자 수').replace('clearCnt', '격리해제 수').replace('examCnt', '검사진행 수').replace('deathCnt', '사망자 수').replace('careCnt', '치료중 환자 수').replace('resutlNegCnt', '결과 음성 수').replace('accExamCnt', '누적 검사 수').replace('accExamCompCnt', '누적 검사 완료 수').replace('accDefRate', '누적 환진률').replace('createDt', '등록일시분초').replace('updateDt', '수정일시분초')

    js = json.loads(jsonString)
    # 파싱한 전체 결과 보기.
    #print(js)
    js_check_count = js["response"]['body']['items']['item'][0]['검사진행 수']
    js = js["response"]['body']['items']['item']
    pdata = pd.DataFrame(js)

    # 원하는 정보만 파싱한 결과
    # 누적 검사자 수와 누적 확진자수를 제공하기 때문에
    # 전일과의 차이로 일일 확진자, 검사자 수를 구했다.

    print('전일 검사 확진자수 : ',int(pdata.loc[0][7]) - int(pdata.loc[1][7]))
    print('전일 코로나 검사 수',int(pdata.loc[0][8]))

# 함수 정의부
def get_speech():
    # 마이크에서 음성을 추출하는 객체
    recognizer = sr.Recognizer()

    # 마이크 설정
    microphone = sr.Microphone(sample_rate=16000)

    # 마이크 소음 수치 반영
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("소음 수치 반영하여 음성을 청취합니다. {}".format(recognizer.energy_threshold))

    # 음성 수집
    with microphone as source:
        print("Say something!")
        result = recognizer.listen(source)
        audio = result.get_raw_data()
    
    return audio

def kakao_stt(app_key, stype, data):
    if stype == 'stream':
        audio = data
        
    headers = {
        "Content-Type": "application/octet-stream",
        "Authorization": "KakaoAK " + app_key,
    }

    # 카카오 음성 url
    kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    # 카카오 음성 api 요청
    res = requests.post(kakao_speech_url, headers=headers, data=audio)
    # 요청에 실패했다면,
    if res.status_code != 200:
        text=""
        print("error! because ",  res.json())
    else: # 성공했다면,
    	  #print("음성인식 결과 : ", res.text)
          #print("시작위치 : ", res.text.index('{"type":"finalResult"'))
          #print("종료위치 : ", res.text.rindex('}')+1)
          #print("추출한 정보 : ", res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1])
        try:
            result = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
            text = json.loads(result).get('value')
        except:
            text = "speak again"

    return text



# 함수 호출부
KAKAO_APP_KEY = "48995414c941eef20bfff6ad9c023947"
audio = get_speech()
text = kakao_stt(KAKAO_APP_KEY, "stream", audio)
print("음성 인식 결과 : " + text) 

#날씨
valWeather = "날씨" in text
if valWeather:
    weather()

#노래
valMusic = "노래" in text
if valMusic:
    music()

#코로나확진현황
valCovid = "코로나" in text
if valCovid:
    covid()