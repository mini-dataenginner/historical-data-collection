import ccxt
import datetime
import time

exchange = ccxt.upbit()
exchange.load_markets()

symbol = 'BTC/KRW'
timeframe = '1m'  # 1분 봉
limit = 200       # 한번에 가져올 수 있는 최대 캔들 수

start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = start_date + datetime.timedelta(days=1)  # 하루 뒤(1년 전 날짜의 하루치 수집)
since = int(start_date.timestamp() * 1000)

all_ohlcv = []

print(f"📌 요청한 시작 날짜: {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📌 요청한 종료 날짜: {end_date.strftime('%Y-%m-%d %H:%M:%S')}\n")

while True:
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    if not ohlcv:
        break
    
    # 이번에 가져온 데이터 중 end_date를 초과하는 부분은 제외
    filtered_ohlcv = []
    for candle in ohlcv:
        ts = candle[0]  # 타임스탬프 (밀리초)
        if ts < int(end_date.timestamp() * 1000):
            filtered_ohlcv.append(candle)
        else:
            break  # end_date를 넘어가는 캔들은 무시하고 종료
    
    all_ohlcv.extend(filtered_ohlcv)

    if filtered_ohlcv:
        last_timestamp = filtered_ohlcv[-1][0]
        since = last_timestamp + 1
    else:
        break

    if len(ohlcv) < limit or (filtered_ohlcv and filtered_ohlcv[-1][0] >= int(end_date.timestamp() * 1000)):
        break

    time.sleep(exchange.rateLimit / 1000)

print(f"✅ 가져온 1분봉 OHLCV 데이터 개수: {len(all_ohlcv)}\n")

if all_ohlcv:
    first_candle = all_ohlcv[0]
    last_candle = all_ohlcv[-1]
    
    first_timestamp = first_candle[0]
    last_timestamp = last_candle[0]

    first_time = datetime.datetime.fromtimestamp(first_timestamp / 1000)
    last_time = datetime.datetime.fromtimestamp(last_timestamp / 1000)

    print(f"📌 가장 과거 데이터: {first_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📌 가장 최근 데이터: {last_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 샘플 데이터 5개 출력
    print("📊 수집된 데이터 샘플 (최근 5개):")
    for candle in all_ohlcv[-5:]:
        timestamp, open_price, high_price, low_price, close_price, volume = candle
        candle_time = datetime.datetime.fromtimestamp(timestamp / 1000)
        print(f"{candle_time.strftime('%Y-%m-%d %H:%M:%S')}, 시가: {open_price}, 고가: {high_price}, 저가: {low_price}, 종가: {close_price}, 거래량: {volume}")

else:
    print("❌ 데이터를 가져오지 못했습니다.")
