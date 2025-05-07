import streamlit as st

st.sidebar.page_link("pages/1_Home.py", label="홈")
st.sidebar.page_link("pages/2_Chatbot.py", label="Chatbot")

st.set_page_config(page_title="AI 멀티페이지 앱", layout="centered")
st.title("🎉 AI 웹앱에 오신 걸 환영합니다!")
st.markdown("👉 왼쪽 사이드바에서 **Chatbot**을 클릭해 대화를 시작해보세요.")
