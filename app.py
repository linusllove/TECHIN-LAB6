import os
import streamlit as st
import fitz  # PyMuPDF
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit page configuration
st.set_page_config(
    page_title="ElioChat",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="auto"
)

openai.api_key = OPENAI_API_KEY

def read_pdf(file):
    """Read and extract text from uploaded PDF file."""
    text = ""
    with fitz.open(stream=file) as doc:
        for page in doc:
            text += page.get_text()
    return text

def generate_activities_report(text):
    """Generate a report on activities for kids from the text using OpenAI."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Generate a report on activities for kids mentioned in the text: \n" + text,
        temperature=0.5,
        max_tokens=1024,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# File uploader widget
uploaded_file = st.file_uploader("Upload a file", type=["pdf"])
if uploaded_file:
    with st.spinner("Reading and analyzing the document..."):
        text = read_pdf(uploaded_file)
        report = generate_activities_report(text)
        st.subheader("Activities Analysis Report")
        st.write(report)

# Instructions
st.write("Upload a PDF document containing information about activities for kids to generate an activities analysis report.")
