import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="Solar AI Assistant", page_icon="☀️", layout="wide")

st.markdown(
    """
    <style>
        /* Set max-width for the main content */
        .block-container {
            max-width: 1300px;
            width: 100%;
            margin: auto;
        }
        
        /* Change the font */
        html, body, .stApp {
            font-family: 'Poppins', sans-serif;
        }

        /* Style the input box */
        .stTextInput > div > div > input {
            border-radius: 8px;
        }

        /* Style buttons */
        .stButton>button {
            background-color: #0077b6 !important;
            color: white !important;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border: none;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌞 Solar AI Assistant")
st.subheader("💡 Get expert insights on solar energy!")

user_query = st.text_input("Ask me anything about solar energy...", "")

def get_solar_advice(query):
    if not API_KEY:
        return "❌ API key missing! Please set up your .env file."
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [{"role": "user", "content": query}]
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        response_data = response.json()
        print("🔍 Full Response:", json.dumps(response_data, indent=2))
        
        if "choices" in response_data:
            return response_data["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Unexpected response format: {response_data}"
    except Exception as e:
        return f"⚠️ Error: {e}"

if st.button("🔍 Get Answer"):
    if user_query:
        answer = get_solar_advice(user_query)
        st.write("### ⚡ Response:")
        st.write(answer)
    else:
        st.warning("Please enter a question!")
