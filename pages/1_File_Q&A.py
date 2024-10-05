import streamlit as st
import os
import toml
import google.generativeai as genai
import time

# Load the .rff.toml file
config_path = os.path.join(os.path.dirname(__file__), '..', '.ruff.toml')
if os.path.exists(config_path):
    config = toml.load(config_path)
    gemini_api_key = config.get('api_key')
else:
    st.error("Config file not found. Please ensure .rff.toml exists in the project root.")
    st.stop()

if not gemini_api_key:
    st.error("Gemini API key not found in config. Please add it to .rff.toml")
    st.stop()

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

st.title("📝 File Q&A with Gemini API")

# File uploader
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))

# Initialize session state
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'file_uri' not in st.session_state:
    st.session_state.file_uri = None
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None

# Upload file if not already done
if uploaded_file and not st.session_state.file_uploaded:
    with st.spinner("Uploading file..."):
        # Save the uploaded file temporarily
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Upload the file to Gemini
        file = genai.upload_file(uploaded_file.name, mime_type="application/pdf" if uploaded_file.name.endswith(".pdf") else "text/plain")
        st.session_state.file_uri = file.uri
        st.write(f"Uploaded file '{file.display_name}' as: {file.uri}")

        # Wait for the file to be ready for processing
        while file.state.name == "PROCESSING":
            st.write("Waiting for file processing...")
            time.sleep(10)
            file = genai.get_file(file.name)
        
        if file.state.name != "ACTIVE":
            st.error(f"File {file.name} failed to process")
            st.stop()
        
        st.success("File processed successfully!")
        st.session_state.file_uploaded = True

        # Create the model and start the chat session
        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        st.session_state.chat_session = model.start_chat(history=[
            {
                "role": "user",
                "parts": [file],
            },
        ])

# Question input
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not st.session_state.file_uploaded,
)

# Process question
if st.session_state.file_uploaded and question:
    with st.spinner("Generating answer..."):
        response = st.session_state.chat_session.send_message(question)
        st.write("### Answer")
        st.write(response.text)

# Cleanup: remove the temporary file
# if st.session_state.file_uploaded:
    # os.remove(uploaded_file.name)