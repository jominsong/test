import streamlit as st
from openai import OpenAI

# OpenAI API 키 입력
api_key = st.text_input("OpenAI API Key", type="password")
if api_key:
    cached_key = store_api_key(api_key)
    st.success("API 키가 캐시에 저장되었습니다.")
    st.write(f"저장된 API 키 (디버그용): {cached_key}")
# 클라이언트 초기화 (API 키가 입력된 경우에만)
if api_key:
    client = OpenAI(api_key=api_key)

    st.title("OpenAI GPT model")

    prompt = st.text_area("User prompt")

    if st.button("Ask!", disabled=(len(prompt) == 0)):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        st.write(response.output_text)

    # Session state 예시
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'

    # 키 삭제 예시
    del st.session_state["key"]
else:
    st.warning("API 키를 입력해주세요.")
# 위젯을 이용한 session_state 저장
st.text_input("Your name", key="name")
st.session_state.name

with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)

@st.cache_data
def store_api_key(key: str):
    return key # 단순히 key를 반환하지만 캐시에 저장됨

