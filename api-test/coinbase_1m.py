"""
코인 베이스 1분봉 캔들 데이터 수집 스크립트.

이 스크립트는 코인 베이스 API를 사용하여 과거 1분봉 캔들스틱 데이터를 가져옵니다.
"""


import json
from datetime import datetime, timedelta
import requests

# Coinbase API 엔드포인트
BASE_URL = "https://api.exchange.coinbase.com/products"

def get_all_historical_candles(product_id="BTC-USD", granularity=86400):
    """
    Coinbase에서 특정 상품(product_id)의 모든 과거 시세 데이터를 가져온다.
    :param product_id: 조회할 거래 상품 (ex. BTC-USD, ETH-USD)
    :param granularity: 캔들 간격 (초 단위) - {60, 300, 900, 3600, 21600, 86400} 중 하나
    :return: 전체 캔들 데이터 리스트
    """

    all_data = []  # 모든 데이터를 저장할 리스트
    end_time = datetime.utcnow()  # 현재 시간부터 시작

    while True:
        start_time = end_time - timedelta(seconds=granularity * 300)  # 300개 데이터 분량씩 요청
        params = {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "granularity": granularity,
        }

        url = f"{BASE_URL}/{product_id}/candles"
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, Message: {response.text}")
            break  # 에러 발생 시 종료

        data = response.json()

        if not data:
            print("✅ 모든 데이터를 가져왔습니다.")
            break  # 더 이상 데이터가 없으면 종료

        all_data.extend(data)  # 데이터 추가
        end_time = start_time  # 다음 요청을 위해 end_time 업데이트

        print(f"📦 {len(data)}개 데이터 수집 완료 (현재: {start_time.date()})")

    print("\n🔥 모든 데이터 수집 완료!")
    print(json.dumps(all_data[:5], indent=4))  # 상위 5개 데이터 출력

    return all_data

# 실행 코드
if __name__ == "__main__":
    print("Fetching all historical candles data from Coinbase...\n")
    all_candles = get_all_historical_candles(product_id="BTC-USD", granularity=86400)
