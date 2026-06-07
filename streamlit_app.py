import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from rag import build_rag_chain

load_dotenv()

st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄"
)

st.title("📄 PDF Question Answering System")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    if "rag_chain" not in st.session_state:

        with st.spinner("Processing PDF..."):
            st.session_state.rag_chain = build_rag_chain(
                pdf_path
            )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input(
        "Ask a question about the PDF..."
    )

    if query:

        st.session_state.messages.append(
            {"role": "user", "content": query}
        )

        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Generating answer..."):
            answer = st.session_state.rag_chain.invoke(
                query
            )

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )