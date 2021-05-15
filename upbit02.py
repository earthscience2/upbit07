import time
import pyupbit
import datetime
import requests

now = datetime.datetime.now()

access = "bAxXjSkcPIOQZKwiECpJTyXyUkG9oICbqi1SIjwR"
secret = "UOk6txTV0XarEx0L2QcluxZv6SuI3HQw6xITrscw"
myToken = "..."

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text})   
    
while True:
    try:
        #현재 시간 조회
        now = time.localtime()
        #도지코인 현재시세, 현재가격
        doge_now_price = pyupbit.get_current_price("KRW-DOGE"), "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        #도지코인 현재 평균 거래량
        doge_df2 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=1)
        doge_vma1 = doge_df2['volume'].rolling(1).mean().iloc[-1]
        #도지코인 5일 평균 거래량
        doge_df1 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=5)
        doge_vma5 = doge_df1['volume'].rolling(5).mean().iloc[-1]
        #도지코인 현재 이동 평균선 조회
        doge_df3 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=1)
        doge_ma1 = doge_df3['close'].rolling(1).mean().iloc[-1]
        #도지코인 5일 이동 평균선 조회
        doge_df4 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=5)
        doge_ma5 = doge_df4['close'].rolling(5).mean().iloc[-1]
        #도지코인 30일 이동 평균선 조회
        doge_df5 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=30)
        doge_ma30 = doge_df5['close'].rolling(30).mean().iloc[-1]
        #도지코인 120일 이동 평균선 조회
        doge_df6 = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=120)
        doge_ma120 = doge_df6['close'].rolling(120).mean().iloc[-1]
        
        if doge_vma1 > doge_vma5 and doge_ma1 > doge_ma5 > doge_ma30 > doge_ma120:
            print("도지코인 매수 타이밍")
            print(doge_now_price)
            post_message(myToken,"#bitcoin-stock", "도지코인-----매수 타이밍-----" +str(doge_now_price))
        
        elif doge_vma5 > doge_vma1 and doge_ma5 > doge_ma1: 
            print("도지코인 매도 타이밍")
            print(doge_now_price)
            post_message(myToken,"#bitcoin-stock", "도지코인-----매도 타이밍-----" +str(doge_now_price))
            
        else:
            print("도지코인 관망")
            print(doge_now_price)
            post_message(myToken,"#bitcoin-stock", "도지코인-----관망-----" +str(doge_now_price))


        #비트코인 현재시세, 현재가격
        btc_now_price = pyupbit.get_current_price("KRW-BTC"), "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        #비트코인 현재 평균 거래량
        btc_df2 = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1)
        btc_vma1 = btc_df2['volume'].rolling(1).mean().iloc[-1]
        #비트코인 5일 평균 거래량
        btc_df1 = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=5)
        btc_vma5 = btc_df1['volume'].rolling(5).mean().iloc[-1]
        #비트코인 현재 이동 평균선 조회
        btc_df3 = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1)
        btc_ma1 = btc_df3['close'].rolling(1).mean().iloc[-1]
        #비트코인 5일 이동 평균선 조회
        btc_df4 = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=5)
        btc_ma5 = btc_df4['close'].rolling(5).mean().iloc[-1]
        #비트코인 30일 이동 평균선 조회
        btc_df5 = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=30)
        btc_ma30 = btc_df5['close'].rolling(30).mean().iloc[-1]
        #비트코인 120일 이동 평균선 조회
        btc_df6 = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=120)
        btc_ma120 = btc_df6['close'].rolling(120).mean().iloc[-1]
    
    
        if btc_vma1 > btc_vma5 and btc_ma1 > btc_ma5 > btc_ma30 > btc_ma120:
            print("비트코인 매수 타이밍")
            print(btc_now_price)
            post_message(myToken,"#bitcoin-stock", "비트코인-----매수 타이밍-----" +str(btc_now_price))

        elif btc_vma5 > btc_vma1 and btc_ma5 > btc_ma1: 
            print("비트코인 매도 타이밍")
            print(btc_now_price)
            post_message(myToken,"#bitcoin-stock", "비트코인-----매도 타이밍-----" +str(btc_now_price))
            
        else:
            print("비트코인 관망")
            print(btc_now_price)
            post_message(myToken,"#bitcoin-stock", "비트코인-----관망-----" +str(btc_now_price))
            
        time.sleep(10)
        
    except Exception as e:
        print("ERROR")
        post_message(myToken,"bitcoin-stock", "에러발생----살려줘-----")
        
        time.sleep(1) 
