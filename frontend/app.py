import streamlit as st
import requests
import json
import os

# Page Config
st.set_page_config(
    page_title="DevOps AI Agent",
    page_icon="🚀",
    layout="wide"
)

# Dark Mode / Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🚀 DevOps LLM SaaS Agent")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Settings")
    if st.button("🔄 Refresh Knowledge Base"):
        with st.spinner("Re-indexing docs..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/ingest")
                if resp.status_code == 200:
                    st.success("Indexed!")
                else:
                    st.error("Failed to index.")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.info("Ask about Docker, Kubernetes, Terraform, or company-specific DevOps workflows.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a DevOps question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consulting the documentation..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"query": prompt}
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    
                    st.markdown(answer)
                    if sources:
                        with st.expander("Sources"):
                            for s in sources:
                                st.write(f"- {s}")
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("API error.")
            except Exception as e:
                st.error(f"Connection error: {e}")
