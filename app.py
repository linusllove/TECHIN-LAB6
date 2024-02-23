from tempfile import NamedTemporaryFile
import os
import re

import streamlit as st
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Classify Kids' Activities",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

def classify_activities(docs):
    categories = {
        "Outdoor": ["park", "hiking", "beach"],
        "Educational": ["museum", "library", "reading"],
        "Sports": ["soccer", "basketball", "swimming"],
        "Arts & Crafts": ["painting", "drawing", "crafts"],
    }
    results = {}
    for doc in docs:
        for category, keywords in categories.items():
            if any(keyword in doc.lower() for keyword in keywords):
                results.setdefault(category, []).append(doc)
    return results

if "classification_results" not in st.session_state.keys():  # Initialize the classification results
    st.session_state.classification_results = {}

uploaded_file = st.file_uploader("Upload a document file")
if uploaded_file:
    bytes_data = uploaded_file.read()
    with NamedTemporaryFile(delete=False) as tmp:  # Open a named temporary file
        tmp.write(bytes_data)  # Write data from the uploaded file into it
        with st.spinner("Extracting and classifying activities from your document..."):
            reader = PDFReader()
            docs = reader.load_data(tmp.name)
            st.session_state.classification_results = classify_activities(docs)
    os.remove(tmp.name)  # Remove temp file

if st.session_state.classification_results:
    for category, activities in st.session_state.classification_results.items():
        st.subheader(category)
        for activity in activities:
            st.write("- ", activity)
else:
    st.write("Upload a document to classify kids' activities.")

