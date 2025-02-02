import requests
import time
import datetime

# 1년 전의 Unix Timestamp 계산 (밀리초 단위)
one_year_ago = int((datetime.datetime.utcnow() - datetime.timedelta(days=365)).timestamp() * 1000)

# 현재 시간의 Unix Timestamp (밀리초 단위)
now = int(time.time() * 1000)

# 바이낸스 API 엔드포인트
url = "https://api.binance.com/api/v3/klines"

# 요청 파라미터 설정
params = {
    "symbol": "BTCUSDT",  # 원하는 거래쌍
    "interval": "1m",  # 1일 간격의 데이터
    "startTime": one_year_ago,  # 1년 전
    "endTime": now,  # 현재 시간
    "limit": 1000  # 최대 1000개 데이터 (필요시 반복 요청)
}

# API 요청
response = requests.get(url, params=params)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()
    for candle in data:
        timestamp = datetime.datetime.utcfromtimestamp(candle[0] / 1000)
        open_price = candle[1]
        close_price = candle[4]
        print(f"{timestamp}: Open={open_price}, Close={close_price}")
else:
    print(f"Error: {response.status_code}, {response.text}")
