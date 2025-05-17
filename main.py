import streamlit as st  # Import Streamlit first

# Set the page configuration as the very first Streamlit command.
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon="🧠",
    layout="centered",
)

import os
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API key is loaded properly
# if not GOOGLE_API_KEY:
#     st.error("❌ Google API key not found. Please set it in your .env file.")
#     st.stop()
# else:
#     st.success("✅ API Key loaded successfully.")

# Configure the Gemini API with the key
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini-Pro model
model = gen_ai.GenerativeModel("gemini-2.0-flash")

# Function to map Gemini roles to Streamlit chat UI roles
def translate_role(role):
    return "assistant" if role == "model" else role

# Start or retrieve chat session from the session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the app title
st.title("🤖 Welcome to Neural Nexus")

# Display chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(translate_role(msg.role)):
        st.markdown(msg.parts[0].text)

# Input field for user prompt
user_prompt = st.chat_input("Ask something...")

# Process new user message
if user_prompt:
    # Display user's message
    st.chat_message("user").markdown(user_prompt)

    # Send message to Gemini-Pro and get the response
    response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's reply
    with st.chat_message("assistant"):
        st.markdown(response.text)