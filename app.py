import streamlit as st
from crawl_posco_news import search_news
from datetime import datetime
from email.utils import parsedate_to_datetime

# 페이지 설정
st.set_page_config(
    page_title="뉴스 검색",
    page_icon="📰",
    layout="wide"
)

# 스타일 설정
st.markdown("""
<style>
    .news-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: box-shadow 0.3s;
    }
    .news-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .news-title {
        font-size: 27px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .news-meta {
        font-size: 13px;
        color: #666;
        margin-bottom: 12px;
    }
    .news-date {
        color: #999;
        font-size: 16px;
    }
    .news-link {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        text-decoration: none;
        margin-top: 10px;
        font-weight: 500;
    }
    .news-link:hover {
        background-color: #1557a0;
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.title("📰 뉴스 검색")
st.markdown("---")

# 초기값 설정
if "search_keyword" not in st.session_state:
    st.session_state.search_keyword = "포스코"
if "initial_search" not in st.session_state:
    st.session_state.initial_search = True

# 검색 입력 UI (Form 사용으로 엔터키 감지) - 왼쪽 절반만 차지
left_col, right_col = st.columns([1, 1])

with left_col:
    with st.form("search_form", border=False):
        col1, col2, col3, col4 = st.columns([0.6, 0.3, 0.7, 0.7], vertical_alignment="center")
        with col1:
            search_keyword = st.text_input("",
                value=st.session_state.search_keyword,
                placeholder="검색 키워드 입력",
                label_visibility="collapsed",
                key="search_input")
        with col2:
            sort_option = st.radio(
                "정렬 방식",
                options=["최신순", "정확도순"],
                horizontal=True,
                label_visibility="collapsed"
            )
        with col3:
            display_count = st.selectbox(
                "기사 갯수",
                options=[20, 50, 100],
                index=0,
                label_visibility="collapsed"
            )
        with col4:
            search_button = st.form_submit_button("🔍 검색", use_container_width=True)

st.markdown("---")

# 정렬 옵션을 API 파라미터로 변환
sort_value = "date" if sort_option == "최신순" else "sim"

# 검색 실행 조건 (초기 로드 또는 form 제출)
if (search_keyword and search_button) or (st.session_state.initial_search and search_keyword):
    st.session_state.initial_search = False
    # crawl_posco_news.py에서 search_news() 함수로 뉴스 데이터 가져오기
    result = search_news(search_keyword, display=display_count, sort=sort_value)

    # 오류 확인
    if result.get("error"):
        st.error(f"❌ {result.get('message')}")
    else:
        items = result.get("items", [])

        if items:
            st.markdown(f"#### '{search_keyword}' 검색 결과 (최신순 상위 {len(items)}개 기사)")

            # 2열로 기사 카드 표시
            cols = st.columns(2, gap="medium")
            for idx, item in enumerate(items, 1):
                # HTML 태그 제거
                title = item.get("title", "").replace("<b>", "").replace("</b>", "").replace("&quot;", '"')
                description = item.get("description", "").replace("<b>", "").replace("</b>", "").replace("&quot;", '"')
                source = item.get("source", "")
                pub_date_raw = item.get("pubDate", "")
                link = item.get("link", "")

                # 날짜 형식 변환 (RFC 2822 -> yyyy-mm-dd hh:mm 요일)
                try:
                    date_obj = parsedate_to_datetime(pub_date_raw)
                    # 한국어 요일
                    days_kr = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
                    day_name = days_kr[date_obj.weekday()]
                    pub_date = date_obj.strftime(f"%Y-%m-%d %H:%M") + f" {day_name}"
                except:
                    pub_date = pub_date_raw

                # 홀수/짝수에 따라 다른 컬럼에 표시
                col_idx = (idx - 1) % 2
                with cols[col_idx]:
                    # 카드 렌더링
                    st.markdown(f"""
                    <div class="news-card">
                        <div class="news-title">{title}</div>
                        <div class="news-meta">
                            <span class="news-date">{pub_date}</span>
                        </div>
                        <p>{description}</p>
                        <a href="{link}" target="_blank" class="news-link">기사 보기 →</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning(f"'{search_keyword}'에 대한 검색 결과가 없습니다.")

else:
    st.info("🔎 위의 검색창에 키워드를 입력하고 '검색' 버튼을 클릭하세요.")

# 하단 정보
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px;">
    뉴스 검색 | Powered by Naver Search API
</div>
""", unsafe_allow_html=True)
