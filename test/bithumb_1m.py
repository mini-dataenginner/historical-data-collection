"""
빗썸 1분봉 캔들 데이터 수집 스크립트.

이 스크립트는 빗썸 API를 사용하여 과거 1분봉 캔들스틱 데이터를 가져옵니다.
"""


import time
import requests

# 빗썸 API URL
API_URL = "https://api.bithumb.com/v1/candles/minutes/{unit}"


def fetch_candles(market_symbol, time_unit, count=200, to=None):
    """
    캔들 데이터를 요청하는 함수.
    """
    url = API_URL.format(unit=time_unit)
    params = {
        "market": market_symbol,
        "count": count,
    }
    if to:
        params["to"] = to

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except ValueError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Response content: {response.text}")
        return []


def fetch_all_candles(market_symbol, time_unit):
    """
    특정 마켓의 모든 캔들 데이터를 가져오고 최초 데이터를 확인하는 함수.
    """
    all_candles = []
    to = None
    while True:
        candles = fetch_candles(market_symbol, time_unit, to=to)
        if not candles:
            break
        all_candles.extend(candles)

        for candle in candles:
            try:
                print(f"Date: {candle['candle_date_time_kst']}, "
                      f"Open: {candle['opening_price']}, "
                      f"Close: {candle['closing_price']}, "
                      f"Low: {candle['low_price']}, "
                      f"Volume: {candle['candle_acc_trade_volume']}")
            except KeyError as e:
                print(f"Missing expected field: {e}")
                print(f"Raw candle data: {candle}")

        to = candles[-1]["candle_date_time_utc"]
        time.sleep(0.1)

    return all_candles


if __name__ == "__main__":
    MARKET_SYMBOL = "KRW-BTC"
    TIME_UNIT = 1
    print(f"Fetching all candles for {MARKET_SYMBOL} with {TIME_UNIT}-minute intervals...\n")
    candle_data = fetch_all_candles(MARKET_SYMBOL, TIME_UNIT)
