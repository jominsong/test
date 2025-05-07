import streamlit as st
from openai import OpenAI

# 캐시에 API 키를 저장하는 함수
@st.cache_data
def store_api_key(key: str):
    return key

# 메모리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메시지 사용자/응답 구분해서 보여주기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# OpenAI API 키 입력
input_key = st.text_input("OpenAI API Key", type="password")

if input_key:
    cached_key = store_api_key(input_key)
    client = OpenAI(api_key=input_key)

    st.success("API 키가 캐시에 저장되었습니다.")
    st.write(f"저장된 API 키 (디버그용): {cached_key}")

    st.title("OpenAI GPT model")
    prompt = st.text_area("원하는 내용을 입력해주세요")

    if st.button("Ask!", disabled=(len(prompt) == 0)):
        # 사용자 메시지 저장 및 출력
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # GPT 응답 받기
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        # 응답 출력 및 저장
        reply = response.output_text
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    st.warning("API 키를 입력해주세요.")
