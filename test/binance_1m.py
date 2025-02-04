"""
이 모듈은 바이낸스 API에서 BTC/USDT의 과거 1분 봉 데이터를 가져옵니다.
"""

from datetime import datetime, timedelta
import requests

# Binance API 엔드포인트 (상수는 대문자로)
BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

# 1년 전과 현재 시간의 Unix Timestamp (밀리초 단위)
ONE_YEAR_AGO = int((datetime.utcnow() - timedelta(days=365)).timestamp() * 1000)
NOW = int(datetime.utcnow().timestamp() * 1000)

# 요청 파라미터 설정
PARAMS = {
    "symbol": "BTCUSDT",
    "interval": "1m",
    "startTime": ONE_YEAR_AGO,
    "endTime": NOW,
    "limit": 1000
}

def fetch_binance_data():
    """Binance API에서 1년 전부터 현재까지의 1분 봉 데이터를 가져온다."""
    response = requests.get(BINANCE_API_URL, params=PARAMS, timeout=10)
    if response.status_code == 200:
        data = response.json()
        for candle in data:
            timestamp = datetime.utcfromtimestamp(candle[0] / 1000)  # UTC 변환
            open_price = candle[1]
            close_price = candle[4]
            print(f"{timestamp}: Open={open_price}, Close={close_price}")
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    fetch_binance_data()
