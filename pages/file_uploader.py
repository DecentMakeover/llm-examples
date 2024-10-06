import streamlit as st

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file locally
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display PDF using an iframe with file path
    pdf_display = f'<iframe src="temp.pdf" width="700" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
