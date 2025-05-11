# pages/2_Chatbot.py

import streamlit as st

st.title("💬 Chatbot")

# 여기 GPT 연결 코드, 채팅 UI 넣기
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
    if prompt := st.chat_input("도서관 규정에 관한 궁금한 내용을 여기에 입력해주세요"):
        # 사용자 메시지 저장 및 출력
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # GPT 응답
     # 규정 요약 - system prompt로 전달
system_prompt = """
너는 부경대학교 도서관 규정을 잘 아는 AI야. 사용자의 질문에 다음 규정 내용을 바탕으로 성실하게 답해줘.

[규정 요약]
- 도서관 목적: 자료 확보, 직원 배치, 효율적 이용 등
- 이용 대상: 교직원, 재학생, 관장 허가를 받은 외부인
- 대출 권한: 학부생 10권 14일, 대학원생·직원 20권 30일, 교수 50권 90일
- 제한 자료: 논문, 연속간행물, 참고자료, 귀중자료 등
- 반납/제재: 미반납 시 졸업·장학금 제한 등 가능
"""

# GPT Chat Completion API 사용
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)
reply = response.choices[0].message.content

        # GPT 응답 출력 및 저장
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.warning("API 키를 입력해주세요.")
