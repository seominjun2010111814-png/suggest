import os
import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="한 줄 건의함", page_icon="💡", layout="centered")

# 환경 변수에서 Supabase 설정 불러오기
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# 환경 변수 누락 시 경고 표시
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ SUPABASE_URL 또는 SUPABASE_KEY 환경 변수가 설정되지 않았습니다.")
    st.stop()

# Supabase 클라이언트 초기화
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("💡 한 줄 건의함")
st.caption("자유롭게 한 줄로 건의사항을 남겨주세요. (익명)")

# 건의사항 입력 폼
with st.form(key="suggestion_form", clear_on_submit=True):
    category = st.selectbox(
        label="카테고리",
        options=["일반", "시설", "수업/학습", "기타"]
    )
    user_input = st.text_input(
        label="건의 내용",
        placeholder="건의하고 싶은 내용을 입력하세요..."
    )
    submit_button = st.form_submit_button(label="제출하기", use_container_width=True)

# 제출 처리 로직
if submit_button:
    trimmed_input = user_input.strip()
    if not trimmed_input:
        st.warning("내용을 입력해 주세요.")
    else:
        try:
            # Supabase suggestions 테이블에 데이터 삽입
            data = {
                "content": trimmed_input,
                "category": category,
                "likes": 0
            }
            supabase.table("suggestions").insert(data).execute()
            st.success("건의가 접수되었습니다!")
            st.rerun()
        except Exception as e:
            st.error(f"저장 중 오류가 발생했습니다: {e}")

st.divider()

# 건의사항 목록 출력 (최신순)
st.subheader("📋 등록된 건의사항")

try:
    # created_at 기준 내림차순(최신순)으로 데이터 조회
    response = supabase.table("suggestions").select("*").order("created_at", desc=True).execute()
    suggestions = response.data

    if not suggestions:
        st.info("아직 등록된 건의사항이 없습니다.")
    else:
        for item in suggestions:
            cat = item.get("category", "일반")
            content = item.get("content", "")
            likes = item.get("likes", 0)
            st.markdown(f"**[{cat}]** {content} &nbsp;&nbsp; 👍 {likes}")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")