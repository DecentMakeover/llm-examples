import streamlit as st
import fitz  # PyMuPDF
import io

# Step 1: Upload the PDF file
uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

if uploaded_file:
    # Step 2: Get user input for the name
    user_name = st.text_input("Enter your name:", "")

    if user_name and st.button("Generate PDF with Your Name"):
        # Step 3: Open the uploaded PDF and modify it
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_file:
            page = pdf_file.load_page(0)  # Load the first page to modify

            # Define a rectangle area where the name should be placed
            rect = fitz.Rect(50, 50, 300, 100)  # Adjust coordinates as needed
            page.insert_textbox(rect, user_name, fontsize=12, color=(0, 0, 0))

            # Step 4: Save the modified PDF to a BytesIO buffer
            output_buffer = io.BytesIO()
            pdf_file.save(output_buffer)
            pdf_bytes = output_buffer.getvalue()

            # Step 5: Provide a download button for the modified PDF
            st.download_button(
                label="Download Personalized PDF",
                data=pdf_bytes,
                file_name="personalized_document.pdf",
                mime="application/pdf"
            )
