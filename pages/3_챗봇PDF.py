pip install faiss-cpu PyPDF2 openai tiktoken
# pages/3_ChatPDF.py
import streamlit as st
import faiss
import numpy as np
import openai
from PyPDF2 import PdfReader
import tiktoken

# 임베딩 관련 설정
EMBED_MODEL = "text-embedding-ada-002"
DIMENSIONS = 1536  # ada-002 output dimension

# 세션 초기화
if "index" not in st.session_state:
    st.session_state.index = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []

# PDF 업로드
st.title("📄 ChatPDF - 규정 문서 기반 질문")
api_key = st.text_input("OpenAI API Key", type="password")
uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

# Clear 버튼
if st.button("🧹 Clear"):
    st.session_state.index = None
    st.session_state.chunks = []
    st.success("임베딩 초기화 완료")

# PDF 처리 및 벡터화
if uploaded_file and api_key:
    openai.api_key = api_key
    pdf = PdfReader(uploaded_file)
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text.strip().replace("\n", " ") + "\n"

    # 텍스트 분할
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = tokenizer.encode(full_text)
    chunk_size = 500
    token_chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens), chunk_size)]
    text_chunks = [tokenizer.decode(tc) for tc in token_chunks]

    # 임베딩
    embeddings = []
    for chunk in text_chunks:
        resp = openai.Embedding.create(input=[chunk], model=EMBED_MODEL)
        vector = np.array(resp["data"][0]["embedding"], dtype="float32")
        embeddings.append(vector)

    # FAISS 인덱스 생성
    index = faiss.IndexFlatL2(DIMENSIONS)
    index.add(np.array(embeddings))

    st.session_state.index = index
    st.session_state.chunks = text_chunks
    st.success("✅ PDF 임베딩 완료! 질문해보세요.")

# 사용자 질문 → 검색 + GPT 답변
if st.session_state.index and api_key:
    question = st.chat_input("PDF 내용 기반으로 질문하세요!")
    if question:
        # 질문 임베딩
        query_embed = openai.Embedding.create(input=[question], model=EMBED_MODEL)["data"][0]["embedding"]
        query_vec = np.array(query_embed, dtype="float32")

        # 유사도 검색
        D, I = st.session_state.index.search(np.array([query_vec]), k=3)
        related_chunks = [st.session_state.chunks[i] for i in I[0]]

        # 프롬프트 구성
        context = "\n\n".join(related_chunks)
        prompt = f"다음 내용은 문서에서 가져온 일부입니다:\n\n{context}\n\n사용자 질문: {question}\n\n이 내용을 참고하여 정리된 답변을 해줘."

        # GPT 응답 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 업로드된 PDF 문서를 잘 이해하는 도우미야."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response["choices"][0]["message"]["content"]
        st.chat_message("user").markdown(question)
        st.chat_message("assistant").markdown(answer)
