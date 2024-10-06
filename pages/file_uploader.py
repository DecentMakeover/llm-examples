import streamlit as st
import base64

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read the uploaded PDF file
    base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')

    # Create an HTML iframe to display the PDF
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    
    # Use Streamlit's HTML component to display the iframe
    st.components.v1.html(pdf_display, height=800)
