import streamlit as st

st.set_page_config(page_title="AI 멀티페이지 앱", layout="centered")
st.title("🎉 AI 웹앱에 오신 걸 환영합니다!")
st.markdown("👉 왼쪽 사이드바에서 **Chatbot**을 클릭해 대화를 시작해보세요.")
# 사이드바에 페이지 링크 수동 추가 (선택사항)
st.sidebar.page_link("pages/2_Chatbot.py", label="💬 Chatbot")
