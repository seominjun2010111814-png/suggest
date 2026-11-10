import streamlit as st

st.set_page_config(page_title="한 줄 건의함", page_icon="💡", layout="centered")

st.title("💡 한 줄 건의함")
st.caption("자유롭게 한 줄로 건의사항을 남겨주세요. (익명)")

# 세션 상태에 건의사항 목록 초기화 (st.session_state로 수정)
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

# 건의사항 입력 폼
with st.form(key="suggestion_form", clear_on_submit=True):
    user_input = st.text_input(
        label="건의 내용",
        placeholder="건의하고 싶은 내용을 입력하세요...",
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button(label="제출하기", use_container_width=True)

# 제출 처리 logic
if submit_button:
    trimmed_input = user_input.strip()
    if not trimmed_input:
        st.warning("내용을 입력해 주세요.")
    else:
        # 최신순 정렬을 위해 리스트 맨 앞에 추가
        st.session_state.suggestions.insert(0, trimmed_input)
        st.success("건의가 접수되었습니다!")
        st.rerun()

st.divider()

# 건의사항 목록 출력
st.subheader("📋 등록된 건의사항")

if not st.session_state.suggestions:
    st.info("아직 등록된 건의사항이 없습니다.")
else:
    for idx, item in enumerate(st.session_state.suggestions, start=1):
        st.write(f"• {item}")