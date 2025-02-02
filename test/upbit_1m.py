import requests
import datetime
import time

# Upbit API 엔드포인트
UPBIT_API_URL = "https://api.upbit.com/v1/candles/minutes/1"  # 1분봉 캔들 데이터

# 심볼 설정 (BTC/KRW)
symbol = "KRW-BTC"

# 1년 전의 특정 날짜 기준으로 하루 동안의 데이터를 가져오기
target_date = datetime.datetime(2024, 1, 1, 0, 0, 0)  # 원하는 날짜 설정 (UTC 기준)
start_date = target_date
end_date = start_date + datetime.timedelta(days=1)  # 하루치 데이터 수집

# Upbit API의 `to` 파라미터는 UTC 기준 RFC 3339 형식으로 설정해야 함
to = end_date.strftime('%Y-%m-%dT%H:%M:%S')  # UTC 기준

# 수집된 데이터 리스트
all_ohlcv = []

print(f"📌 요청한 시작 날짜 (UTC): {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📌 요청한 종료 날짜 (UTC): {end_date.strftime('%Y-%m-%d %H:%M:%S')}\n")

while True:
    # API 요청 파라미터
    params = {
        "market": symbol,
        "to": to,
        "count": 200,  # 최대 200개 요청 가능
    }

    headers = {"accept": "application/json"}

    response = requests.get(UPBIT_API_URL, params=params, headers=headers)

    if response.status_code != 200:
        print(f"❌ API 요청 실패: {response.status_code}, {response.text}")
        break

    ohlcv = response.json()

    if not ohlcv:
        break  # 데이터가 없으면 종료

    # Upbit는 최신 데이터부터 반환하므로, 시간순 정렬을 위해 뒤집어야 함
    ohlcv.reverse()

    # start_date 이전의 데이터는 필터링
    filtered_ohlcv = [candle for candle in ohlcv if candle["candle_date_time_utc"] >= start_date.strftime('%Y-%m-%dT%H:%M:%SZ')]

    all_ohlcv.extend(filtered_ohlcv)

    # 가장 오래된 데이터의 시간을 다음 요청의 기준으로 설정 (UTC)
    if filtered_ohlcv:
        to = filtered_ohlcv[0]["candle_date_time_utc"] + "Z"
    else:
        break  # 더 이상 가져올 데이터가 없으면 종료

    # API 요청 속도 제한을 준수 (Upbit는 초당 10회 제한)
    time.sleep(0.1)

print(f"\n✅ 가져온 1분봉 OHLCV 데이터 개수: {len(all_ohlcv)}\n")

if all_ohlcv:
    first_candle = all_ohlcv[0]
    last_candle = all_ohlcv[-1]

    print(f"📌 가장 과거 데이터: {first_candle['candle_date_time_kst']}, 시가: {first_candle['opening_price']}, 종가: {first_candle['trade_price']}")
    print(f"📌 가장 최근 데이터: {last_candle['candle_date_time_kst']}, 시가: {last_candle['opening_price']}, 종가: {last_candle['trade_price']}\n")

    # 샘플 데이터 5개 출력
    print("📊 수집된 데이터 샘플 (최근 5개):")
    for candle in all_ohlcv[-5:]:
        print(f"{candle['candle_date_time_kst']}, 시가: {candle['opening_price']}, 고가: {candle['high_price']}, 저가: {candle['low_price']}, 종가: {candle['trade_price']}, 거래량: {candle['candle_acc_trade_volume']}")

else:
    print("❌ 데이터를 가져오지 못했습니다.")
