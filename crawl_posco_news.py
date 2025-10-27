import requests
import json
import streamlit as st
import os

# 네이버 뉴스 검색 API 설정
API_URL = "https://openapi.naver.com/v1/search/news.json"

# API 헤더 (환경변수에서 가져오기)
def get_headers():
    """환경변수에서 API 키를 가져와서 헤더 생성"""
    client_id = st.secrets.get("NAVER_CLIENT_ID") or os.getenv("NAVER_CLIENT_ID")
    client_secret = st.secrets.get("NAVER_CLIENT_SECRET") or os.getenv("NAVER_CLIENT_SECRET")

    return {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }


def search_news(keyword, display=20, start=1, sort="date"):
    """
    네이버 뉴스 검색 API를 호출하는 함수

    Parameters:
        keyword (str): 검색 키워드
        display (int): 반환할 결과 개수 (기본값: 20)
        start (int): 검색 시작 위치 (기본값: 1)
        sort (str): 정렬 방식, "date"(최신순) 또는 "sim"(정확도순) (기본값: "date")

    Returns:
        dict: API 응답 데이터 또는 오류 정보
    """
    params = {
        "query": keyword,
        "display": display,
        "start": start,
        "sort": sort
    }

    try:
        # API 요청 (헤더는 함수에서 가져오기)
        headers = get_headers()
        response = requests.get(API_URL, headers=headers, params=params)

        # 응답 상태 확인
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": f"API 요청 실패 - Status Code: {response.status_code}",
                "response": response.text
            }

    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "message": f"요청 중 오류 발생: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "error": True,
            "message": f"JSON 파싱 오류: {str(e)}"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"예상치 못한 오류: {str(e)}"
        }


# 직접 실행 시 테스트
if __name__ == "__main__":
    result = search_news("포스코", display=5)
    print(json.dumps(result, indent=2, ensure_ascii=False))
