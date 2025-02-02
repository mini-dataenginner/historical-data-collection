import ccxt
import datetime
import time

# 거래소 및 시장 정보 설정
exchange = ccxt.upbit()
exchange.load_markets()

symbol = 'BTC/KRW'
timeframe = '1m'  # 1분 봉
limit = 200       # 한번에 가져올 수 있는 최대 캔들 수

# 오늘로부터 정확히 1년 전 날짜를 시작점으로 설정
start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = start_date + datetime.timedelta(days=1)  # 하루 뒤(1년 전 날짜의 하루치 수집)
since = int(start_date.timestamp() * 1000)

all_ohlcv = []

while True:
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    if not ohlcv:
        break
    
    # 이번에 가져온 데이터 중 end_date를 초과하는 부분은 제외
    filtered_ohlcv = []
    for candle in ohlcv:
        ts = candle[0]  # 타임스탬프 (밀리초)
        # end_date 기준 시간을 밀리초 단위로 변환
        if ts < int(end_date.timestamp() * 1000):
            filtered_ohlcv.append(candle)
        else:
            # end_date를 넘어서는 캔들은 무시하고 반복 중단
            break
    
    all_ohlcv.extend(filtered_ohlcv)

    # 만약 이번에 가져온 캔들이 전부 end_date 이전이라면, 
    # 마지막 캔들의 타임스탬프 + 1밀리초를 다음 요청 시작점으로 설정
    if filtered_ohlcv:
        last_timestamp = filtered_ohlcv[-1][0]
        since = last_timestamp + 1
    else:
        # 1개도 해당 구간에 속하지 않는 경우 루프 종료
        break

    # 수집된 캔들이 limit보다 적다면 이후 더 이상 데이터가 없다는 의미
    # 혹은 이미 end_date를 넘어섰으므로 종료
    if len(ohlcv) < limit or (filtered_ohlcv and filtered_ohlcv[-1][0] >= int(end_date.timestamp() * 1000)):
        break

    # API 요청 간격(rateLimit) 준수 (밀리초 단위이므로 초 단위로 변환)
    time.sleep(exchange.rateLimit / 1000)

print(f"가져온 1분봉 OHLCV 데이터 개수: {len(all_ohlcv)}")

# 확인용 출력 (예: 최근 5개만)
for candle in all_ohlcv:
    timestamp, open_price, high_price, low_price, close_price, volume = candle
    candle_time = datetime.datetime.fromtimestamp(timestamp/1000)
    print(candle_time, open_price, high_price, low_price, close_price, volume)
