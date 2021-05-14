import time
import pyupbit
import datetime
import requests

access = "bAxXjSkcPIOQZKwiECpJTyXyUkG9oICbqi1SIjwR"
secret = "UOk6txTV0XarEx0L2QcluxZv6SuI3HQw6xITrscw"
myToken = "xoxb-2052427334483-2052555455970-zqUN73dl8Ducrrl1rY6vKH66"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )                         
while True:
    #"""5일 평균 거래량"""
    df1 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=5)
    vma5 = df1['volume'].rolling(5).mean().iloc[-1]
    #"""현재 평균 거래량"""
    df2 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=1)
    vma1 = df2['volume'].rolling(1).mean().iloc[-1]
    #"""현재 이동 평균선 조회"""
    df3 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=1)
    ma1 = df3['close'].rolling(1).mean().iloc[-1]
    #"""5일 이동 평균선 조회"""
    df4 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=5)
    ma5 = df4['close'].rolling(5).mean().iloc[-1]
    #"""30일 이동 평균선 조회"""
    df5 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=30)
    ma30 = df5['close'].rolling(30).mean().iloc[-1]
    #"""120일 이동 평균선 조회"""
    df6 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=120)
    ma120 = df6['close'].rolling(120).mean().iloc[-1]
    if vma1 > vma5 and ma1 > ma5 > ma30 > ma120:
        print("매수 타이밍")
        post_message(myToken,"#bitcoin-stock", "매수 타이밍")
    elif vma5 > vma1 and ma5 > ma1: 
        print("매도 타이밍")
        post_message(myToken,"#bitcoin-stock", "매도 타이밍")                     
    else:
        print("관망")
        post_message(myToken,"#bitcoin-stock", "관망")
    time.sleep(60)  
