import streamlit as st
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer

# Step 1: Ensure PDF reference is stored in session state
if 'pdf_ref' not in ss:
    ss.pdf_ref = None

# Step 2: File uploader to upload the PDF file
uploaded_file = st.file_uploader("Upload PDF file", type=('pdf'), key='pdf')

if uploaded_file:
    # Store the uploaded file in session state to maintain accessibility during reruns
    ss.pdf_ref = uploaded_file

# Step 3: Display the PDF using the pdf viewer
if ss.pdf_ref:
    # Get the binary data of the uploaded PDF
    binary_data = ss.pdf_ref.getvalue()
    # Display PDF using the pdf_viewer component
    pdf_viewer(input=binary_data, width=700)