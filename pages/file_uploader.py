import streamlit as st
import base64

# Function to display a PDF file
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    show_pdf("temp.pdf")
