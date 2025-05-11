# pages/2_Chatbot.py
import streamlit as st
from openai import OpenAI

st.title("💬 부경대학교 도서관 규정 챗봇")

@st.cache_data
def store_api_key(key: str):
    return key

# 메시지 저장소 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear 버튼
if st.button("Clear Chat"):
    st.session_state.messages = []

# API 키 입력
input_key = st.text_input("OpenAI API Key", type="password")

if input_key:
    cached_key = store_api_key(input_key)
    client = OpenAI(api_key=input_key)

    st.success("API 키가 캐시에 저장되었습니다.")

    # 이전 대화 출력
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("도서관 규정에 대해 질문해보세요!"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 시스템 프롬프트: 규정 요약
        system_prompt = """
        너는 부경대학교 도서관 규정을 기반으로 대답하는 AI야.
        다음 내용을 참고하여 정확하게 답변해줘:

        - 학부생: 최대 10권, 14일
        - 대학원생·직원: 최대 20권, 30일
        - 교수: 최대 50권, 90일
        - 전자책: 모두 5권, 5일
        - 대출 불가: 참고자료, 연속간행물, 학위논문, 귀중자료
        - 미반납 시 졸업·장학금 보류 가능
        """

        # GPT 응답 생성
        response = client.chat.completions.create(
            model="gpt-4",  # 또는 gpt-3.5-turbo
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content

        # 응답 출력 및 저장
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.warning("먼저 OpenAI API 키를 입력해주세요.")
