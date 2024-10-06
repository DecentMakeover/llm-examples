import streamlit as st
import pdfplumber

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        # Extract text from each page and display
        for page in pdf.pages:
            st.text(page.extract_text())
