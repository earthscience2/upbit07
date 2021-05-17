import time
import pyupbit
import datetime
import requests
from pytz import timezone 
from datetime import datetime 

#현재 시간 조회
if __name__ == "__main__":
    fmt = "%Y-%m-%d %H:%M:%S" 
    KST = datetime.now(timezone('Asia/Seoul')) 
    
#개인 정보 입력
access = "bAxXjSkcPIOQZKwiECpJTyXyUkG9oICbqi1SIjwR"
secret = "UOk6txTV0XarEx0L2QcluxZv6SuI3HQw6xITrscw"
myToken = ""

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text})  
    
#구매이력 확인코드
tickers_c = 1

#코인 구매가격
tickers_buy_price = 0

#코인 티커 순서 확인 문자 
a = 0

#현재 시간 조회
if __name__ == "__main__":
    fmt = "%Y-%m-%d %H:%M:%S"

while True:
    try:
        #현재 시간 조회
        KST = datetime.now(timezone('Asia/Seoul')) 
        
        #코인 목록 수 
        coin_num = len(pyupbit.get_tickers(fiat="KRW"))
        
        #코인이름 가져오기
        tickers = pyupbit.get_tickers(fiat="KRW")[a]
        
        #코인 현재시세+현재가격
        tickers_now_price = pyupbit.get_current_price(tickers), KST.strftime(fmt)
        
        #코인 현재시세
        tickers_now_price2 = pyupbit.get_current_price(tickers)
        
        #코인 5분 평균 거래량
        tickers_df1 = pyupbit.get_ohlcv(tickers, interval="minute1", count=5)
        tickers_vma5 = tickers_df1['volume'].rolling(5).mean().iloc[-1]
        #코인 30분 평균 거래량
        tickers_df2 = pyupbit.get_ohlcv(tickers, interval="minute1", count=30)
        tickers_vma30 = tickers_df2['volume'].rolling(30).mean().iloc[-1]
        #코인 현재 이동 평균선 조회
        tickers_df3 = pyupbit.get_ohlcv(tickers, interval="minute1", count=1)
        tickers_ma1 = tickers_df3['close'].rolling(1).mean().iloc[-1]
        #코인 5분 이동 평균선 조회
        tickers_df4 = pyupbit.get_ohlcv(tickers, interval="minute1", count=5)
        tickers_ma5 = tickers_df4['close'].rolling(5).mean().iloc[-1]
        #코인 30분 이동 평균선 조회
        tickers_df5 = pyupbit.get_ohlcv(tickers, interval="minute1", count=30)
        tickers_ma30 = tickers_df5['close'].rolling(30).mean().iloc[-1]
        #코인 120분 이동 평균선 조회
        tickers_df6 = pyupbit.get_ohlcv(tickers, interval="minute1", count=120)
        tickers_ma120 = tickers_df6['close'].rolling(120).mean().iloc[-1]
        

        if  tickers_ma1 > tickers_ma5 > tickers_ma30 > tickers_ma120 and tickers_vma5 > tickers_vma30 :
            print(tickers +" : 매수완료")
            print(tickers_now_price)
            post_message(myToken,"#bitcoin-stock", tickers + " : 매수완료 // 매수가격 : " +str(tickers_now_price))
            a = a + 1
            

        elif tickers_vma30 > tickers_vma5 and tickers_ma5 > tickers_ma1 :
            print(tickers + " : 매도완료")
            print(tickers_now_price)
            post_message(myToken,"#bitcoin-stock", tickers + " : 매도완료 // 매도가격 : " +str(tickers_now_price))
            a = a + 1
        
        elif a == coin_num:
            a = 0
        
        else:
            print(tickers +" : 매매 준비중")
            print(tickers_now_price)
            a = a + 1
              
        time.sleep(0.2)

    except Exception as e:
        print("ERROR")
        a = 0

        time.sleep(50)
