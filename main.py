import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "bcdcfa43-8c3d-4e99-aed1-4a5660cd6b2e"
FLOW_ID = "58a67692-0086-44aa-8f32-d0ea3bc6cb38"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "rag-16000"


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Chat Interface")
    
    message = st.text_area("Message", placeholder="Enter your question")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()