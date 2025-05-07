import streamlit as st
from openai import OpenAI

@st.cache_data
def store_api_key(key: str):
    return key

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔘 Clear 버튼
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()

# 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# API 키 입력
input_key = st.text_input("OpenAI API Key", type="password")

if input_key:
    cached_key = store_api_key(input_key)
    client = OpenAI(api_key=input_key)

    st.success("API 키가 캐시에 저장되었습니다.")

    st.title("OpenAI GPT model")
    prompt = st.text_area("원하는 내용을 입력해주세요")

    if st.button("Ask!", disabled=(len(prompt) == 0)):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        reply = response.output_text
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.warning("API 키를 입력해주세요.")
