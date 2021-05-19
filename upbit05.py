import time
import pyupbit
import datetime
import requests
from decimal import *
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
    
#코인 티커 순서 확인 문자 
a = 0

#구매여부 확인 문자
b = 0

#매수구매 확인 문자
c = 0

#구매가격 확인 문자
d = 0

e = 0

h = 0
#현재 시간 조회
if __name__ == "__main__":
    fmt = "%Y-%m-%d %H:%M:%S"

#구매여부 확인 
buy_time_data = {}

#매수 구매 가격
buy_price = {}

while True:
    try:
        #코인 목록 수
        coin_num = len(pyupbit.get_tickers(fiat="KRW"))
        
        #코인이름 가져오기
        if a < coin_num: 
            tickers = pyupbit.get_tickers(fiat="KRW")[a]
        else:
            tickers = pyupbit.get_tickers(fiat="KRW")[0]

        #구매여부 확인 코드
        if b <= coin_num-1:
            buy_time_data.update({ tickers : True})
            b = b + 1
            
        elif b > coin_num-1:
            b = b + 1
        
        else:
            b = b + 1
            
        #매수 구매 가격 저장코드    
        if c <= coin_num-1:
            buy_price.update({ tickers : 0 })
            c = c + 1
            
        elif c > coin_num-1:
            c = c + 1
        
        else:
            c = c + 1
            
        #현재 시간 조회
        KST = datetime.now(timezone('Asia/Seoul')) 
    
        #코인 현재시세+현재가격
        tickers_now_time_price = pyupbit.get_current_price(tickers), KST.strftime(fmt)
        
        #코인 현재시세
        tickers_now_price2 = int(pyupbit.get_current_price(tickers))
        
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
        
        if a < coin_num-1:
                
            if  buy_time_data[tickers] == True and buy_price[tickers] == 0: 
                 #매수조건
                if tickers_ma1 > tickers_ma5 > tickers_ma30 > tickers_ma120 and tickers_vma5 > tickers_vma30:
                    print(tickers +" : 매수완료")
                    print(tickers_now_time_price)
                    post_message(myToken,"#bitcoin-stock", tickers + " : 매수완료 // 매수가격 : " +str(tickers_now_time_price))
                    buy_time_data.update({ tickers : False })
                    buy_price.update({ tickers : tickers_now_price2 })
                    d = int(buy_price[tickers])
                    a = a + 1
                
                else:     
                    print(tickers +" : 구매전 매수 준비중")
                    print(tickers_now_time_price)
                    a = a + 1
                
                
            elif  buy_time_data[tickers] == False and buy_price[tickers] > 0: 
                
                #매수가격대비 4~%하락시 무조건 매도 
                if  ((( tickers_now_price2 / d ) -1 ) * 100) < -4 and buy_time_data[tickers] == False and buy_price[tickers] > 0:
                    print(tickers + " : 매도완료")
                    print(tickers_now_time_price)
                    post_message(myToken,"#bitcoin-stock", tickers + " : 매도완료 // 매도가격 : " +str(tickers_now_time_price))
                    print(buy_price[tickers])
                    print(tickers_now_price2)
                    d = int(buy_price[tickers])
                    e = int(tickers_now_price2)
                    f = ((( e / d ) - 1 ) * 100 )
                    print("수익률 :" , "%.2f" % (f) , "%")
                    h = f + h
                    print("수익률 합 : ","%.2f" % (h) , "%")
                    post_message(myToken,"#bitcoin-stock", "수익률 : " + "%.2f" % (f) + "%" )
                    buy_time_data.update({ tickers : True}) 
                    buy_price.update({ tickers : 0 })
                    a = a + 1
                
                # 매수가격대비 0~4%하락 and  30평 > 현재가 ---매도
                elif  tickers_vma30 > tickers_vma5 and tickers_ma5 > tickers_ma1 and -4 <= ((( tickers_now_price2 / d ) -1 ) * 100) < 0 and buy_time_data[tickers] == False and buy_price[tickers] > 0:
                    print(tickers + " : 매도완료")
                    print(tickers_now_time_price)
                    post_message(myToken,"#bitcoin-stock", tickers + " : 매도완료 // 매도가격 : " +str(tickers_now_time_price))
                    print(buy_price[tickers])
                    print(tickers_now_price2)
                    d = int(buy_price[tickers])
                    e = int(tickers_now_price2)
                    f = ((( e / d ) - 1 ) * 100 )
                    print("수익률 :" , "%.2f" % (f) , "%")
                    h = f + h
                    print("수익률 합 : ","%.2f" % (h) , "%")
                    post_message(myToken,"#bitcoin-stock", "수익률 : " + "%.2f" % (f) + "%" )
                    buy_time_data.update({ tickers : True}) 
                    buy_price.update({ tickers : 0 })
                    a = a + 1
                
                #매수가격대비 0~6%상승 and 30평 거래량 > 5분 거래량 ---매도
                elif  tickers_vma30 > tickers_vma5 and tickers_ma5 > tickers_ma1 and 0 <= ((( tickers_now_price2 / d ) -1 ) * 100) < 6 and buy_time_data[tickers] == False and buy_price[tickers] > 0:
                    print(tickers + " : 매도완료")
                    print(tickers_now_time_price)
                    post_message(myToken,"#bitcoin-stock", tickers + " : 매도완료 // 매도가격 : " +str(tickers_now_time_price))
                    print(buy_price[tickers])
                    print(tickers_now_price2)
                    d = int(buy_price[tickers])
                    e = int(tickers_now_price2)
                    f = ((( e / d ) - 1 ) * 100 )
                    print("수익률 :" , "%.2f" % (f) , "%")
                    h = f + h
                    print("수익률 합 : ","%.2f" % (h) , "%")
                    post_message(myToken,"#bitcoin-stock", "수익률 : " + "%.2f" % (f) + "%" )
                    buy_time_data.update({ tickers : True}) 
                    buy_price.update({ tickers : 0 })
                    a = a + 1
                
                #매수가격대비 6~%상승시 무조건 매도 
                elif  6 <= ((( tickers_now_price2 / d ) -1 ) * 100)  and buy_time_data[tickers] == False and buy_price[tickers] > 0:
                    print(tickers + " : 매도완료")
                    print(tickers_now_time_price)
                    post_message(myToken,"#bitcoin-stock", tickers + " : 매도완료 // 매도가격 : " +str(tickers_now_time_price))
                    print(buy_price[tickers])
                    print(tickers_now_price2)
                    d = int(buy_price[tickers])
                    e = int(tickers_now_price2)
                    f = ((( e / d ) - 1 ) * 100 )
                    print("수익률 :" , "%.2f" % (f) , "%")
                    h = f + h
                    print("수익률 합 : ","%.2f" % (h) , "%")
                    post_message(myToken,"#bitcoin-stock", "수익률 : " + "%.2f" % (f) + "%" )
                    buy_time_data.update({ tickers : True}) 
                    buy_price.update({ tickers : 0 })
                    a = a + 1

                else:
                    print(tickers +" : 구매후 매도 준비중")
                    print(tickers_now_time_price)
                    a = a + 1
                      
        elif a >= coin_num-1:
            a = 0
            
        else:
            a = 0   
        time.sleep(0.2)

    except Exception as e:
        print("ERROR")
        post_message(myToken,"#bitcoin-stock", "에러발생")
        a = 0

        time.sleep(5)
