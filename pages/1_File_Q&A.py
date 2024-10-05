import streamlit as st
import os
import time
import google.generativeai as genai

# Configure Gemini API key using Streamlit input
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 File Q&A with Gemini API")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not gemini_api_key:
    st.info("Please add your Gemini API key to continue.")

if uploaded_file and question and gemini_api_key:
    # Set the API key for Google Generative AI
    genai.configure(api_key=gemini_api_key)

    # Save the uploaded file temporarily
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Upload the file to Gemini
    def upload_to_gemini(path, mime_type=None):
        file = genai.upload_file(path, mime_type=mime_type)
        return file

    file = upload_to_gemini(uploaded_file.name, mime_type="application/pdf" if uploaded_file.name.endswith(".pdf") else "text/plain")
    st.write(f"Uploaded file '{file.display_name}' as: {file.uri}")

    # Wait for the file to be ready for processing
    def wait_for_files_active(files):
        st.write("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                st.write(".", end="", flush=True)
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        st.write("...all files ready")

    wait_for_files_active([file])

    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    # Start the chat session with the uploaded file and user's question
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    file,
                    question,
                ],
            },
        ]
    )

    # Get the response from the model
    response = chat_session.send_message(question)

    # Display the response
    st.write("### Answer")
    st.write(response.text)