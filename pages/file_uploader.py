import streamlit as st
import pdfplumber
import fitz  # PyMuPDF
import io

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Step 1: Display the PDF content
    with pdfplumber.open(uploaded_file) as pdf:
        for i, page in enumerate(pdf.pages):
            st.write(f"### Page {i + 1}")
            st.text(page.extract_text())

    # Step 2: Get user input for editing
    page_number = st.number_input("Enter the page number to edit", min_value=1, max_value=len(pdf.pages), step=1)
    new_text = st.text_area("Enter the new text to add")

    if st.button("Apply Edits"):
        # Step 3: Modify the PDF using PyMuPDF
        # Load the original PDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # Select the page to edit (note: page_number is 1-based, PyMuPDF uses 0-based index)
        page = pdf_document.load_page(page_number - 1)

        # Add new text at a specified position (you can adjust the position as needed)
        rect = fitz.Rect(50, 50, 550, 100)  # Example rectangle where the text will be added
        page.insert_textbox(rect, new_text, fontsize=12, color=(0, 0, 0))

        # Save the modified PDF to a BytesIO buffer
        pdf_bytes = io.BytesIO()
        pdf_document.save(pdf_bytes)
        pdf_document.close()

        # Step 4: Provide a download link for the modified PDF
        st.download_button(
            label="Download Modified PDF",
            data=pdf_bytes,
            file_name="modified_document.pdf",
            mime="application/pdf"
        )
