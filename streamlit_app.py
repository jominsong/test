import streamlit as st
from openai import OpenAI

# 캐시에 API 키를 저장하는 함수
@st.cache_data
def store_api_key(key: str):
    return key  # 단순히 key를 반환하지만 캐시에 저장됨

# OpenAI API 키 입력
input_key = st.text_input("OpenAI API Key", type="password")

if input_key:
    cached_key = store_api_key(input_key)
    st.success("API 키가 캐시에 저장되었습니다.")
    st.write(f"저장된 API 키 (디버그용): {cached_key}")
        
    client = OpenAI(api_key=input_key)

    st.title("OpenAI GPT model")

    prompt = st.text_area("원하는 내용을 입력해주세요")

    if st.button("Ask!", disabled=(len(prompt) == 0)):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        st.write(response.output_text)

    # Session state 예시
    if 'OpenAI API Key' not in st.session_state:
        st.session_state['OpenAI API Key'] = 'value'

    # 키 삭제 예시
    del st.session_state["OpenAI API Key"]
else:
    st.warning("API 키를 입력해주세요.")





