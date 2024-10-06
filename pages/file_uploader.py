import streamlit as st
import base64

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save PDF to temp location
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Encode PDF to base64
    with open("temp.pdf", "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

    # Embed PDF within iframe
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    st.components.v1.html(pdf_display, height=800)
