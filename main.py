import requests
import streamlit as st
from dotenv import load_dotenv
import os
import base64

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "bcdcfa43-8c3d-4e99-aed1-4a5660cd6b2e"
FLOW_ID = "58a67692-0086-44aa-8f32-d0ea3bc6cb38"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "rag-16000"

st.markdown(
    """
    <style>
    .main {
        background-color: #F7729C;
    }
    .title {
        font-size: 3em;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 1.5em;
        color: #555555;
    }
    .subtext {
        font-size: 1em;
        color: #777777;
    }
    </style>
    """,
    unsafe_allow_html=True
)

current_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(current_dir, "krishna.gif")

# Check if file exists
if os.path.exists(gif_path):
    # Convert the GIF to Base64
    with open(gif_path, "rb") as gif_file:
        gif_base64 = base64.b64encode(gif_file.read()).decode("utf-8")
    
    # Embed the GIF in HTML
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/gif;base64,{gif_base64}" alt="krishna gif" width="650">
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.error(f"GIF file not found: {gif_path}")

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
    st.title("Radhe Radhe..")
    
    message = st.text_area("Message", placeholder="Enter your question to question")
    
    if st.button("Submit"):
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
