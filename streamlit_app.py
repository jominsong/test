import streamlit as st
from openai import OpenAI

@st.cache_data
def store_api_key(key: str):
    return key

# 메시지 저장소 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear Chat 버튼
if st.button("Clear Chat"):
    st.session_state.messages = []

# API 키 입력
input_key = st.text_input("OpenAI API Key", type="password")

if input_key:
    cached_key = store_api_key(input_key)
    client = OpenAI(api_key=input_key)
    st.success("API 키가 캐시에 저장되었습니다.")

    # 이전 대화 모두 보여주기
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ 채팅 입력창 (항상 아래에 고정됨)
    if prompt := st.chat_input("원하는 내용을 입력해주세요"):
        # 사용자 메시지 저장 및 출력
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # GPT 응답
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        reply = response.output_text

        # GPT 응답 출력 및 저장
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.warning("API 키를 입력해주세요.")
