import streamlit as st
import fitz  # PyMuPDF
import io

uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
if uploaded_file:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_file:
        # Example modification (highlight text or other operations)
        page = pdf_file.load_page(0)
        rect = fitz.Rect(50, 50, 150, 100)
        page.insert_textbox(rect, "Sample Text", fontsize=12, color=(1, 0, 0))

        # Save to BytesIO
        output_buffer = io.BytesIO()
        pdf_file.save(output_buffer)
        pdf_bytes = output_buffer.getvalue()

        # Download button for modified PDF
        st.download_button(
            label="Download Modified PDF",
            data=pdf_bytes,
            file_name="modified_document.pdf",
            mime="application/pdf"
        )
