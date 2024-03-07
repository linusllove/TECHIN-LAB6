import streamlit as st
import fitz  # PyMuPDF library
from io import BytesIO

def classify_activities(docs):
    keywords = ["football", "basketball", "soccer", "baseball", "tennis"]
    classification_results = []

    for doc in docs:
        text = ""
        for page in doc:
            text += page.get_text()

        text = text.lower()  # Convert text to lowercase
        if any(keyword in text for keyword in keywords):
            classification_results.append("Sport")
        else:
            classification_results.append("Non-Sport")

    return classification_results

st.title("Activity Classification")

uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])

if uploaded_files:
    docs = []
    for uploaded_file in uploaded_files:
        # 从内存中读取PDF文件
        pdf_bytes = BytesIO(uploaded_file.read())
        docs.append(fitz.open(stream=pdf_bytes, filetype="pdf"))

    st.session_state.classification_results = classify_activities(docs)

    for doc, result in zip(uploaded_files, st.session_state.classification_results):
        st.write(f"{doc.name}: {result}")
