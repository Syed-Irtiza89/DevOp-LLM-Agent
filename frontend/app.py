import streamlit as st
import requests
import json
import os
import time
import random

st.set_page_config(
    page_title="DevOps Copilot Enterprise",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Mode & Mockup-Style SaaS CSS
st.markdown("""
    <style>
    /* Global Background and Typography */
    .stApp {
        background-color: #121418;  /* Deep dark grayish black */
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    .block-container {
        padding-top: 2.5rem;
        max-width: 1500px;
    }
    
    /* Header Typography */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #e2e8f0, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-top: 5px;
        margin-bottom: 30px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* Status Indicator (Green Neon) */
    .status-badge {
        display: flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 8px 16px;
        border-radius: 20px;
        color: #34d399;
        font-weight: 600;
        font-size: 0.9rem;
        float: right;
        margin-top: 15px;
    }
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        box-shadow: 0 0 10px #10b981, 0 0 20px #10b981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Glassmorphism Chat Bubbles */
    .stChatMessage {
        background: #1a1d24 !important; /* Slightly lighter than background */
        border: 1px solid #2d3748 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Code block styling in chat */
    pre {
        background-color: #0f1115 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    code {
        color: #38bdf8 !important; /* light blue code */
    }

    /* Metric Cards in Sidebar */
    .metric-card {
        background: #1a1d24;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 5px;
        display: flex;
        align-items: baseline;
    }
    .metric-delta {
        color: #10b981;
        font-size: 0.9rem;
        margin-left: 10px;
    }

    /* Primary Buttons */
    .stButton>button {
        width: 100%;
        background-color: #3b82f6; /* Blue primary button */
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 0;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Secondary Action Radio (Quick Workflows) */
    div[role="radiogroup"] > label {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        padding: 12px 15px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #3b82f6 !important;
        background-color: #0f172a !important;
    }

    /* Input area */
    .stChatInputContainer {
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        background: #1a1d24 !important;
        padding: 5px !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f1115;
        border-right: 1px solid #1e293b;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: #64748b;
        font-weight: 600;
        font-size: 1.05rem;
    }
    .stTabs [aria-selected="true"] {
        color: #e2e8f0;
        border-bottom: 2px solid #3b82f6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- HEADER NAVIGATION ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1>⚙️ DevOps Copilot Enterprise</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Autonomous Cloud Infrastructure Intelligence</div>", unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class='status-badge'>
            <span class='status-dot'></span>
            System Online
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: #1e293b; margin-top: 0;'>", unsafe_allow_html=True)

# --- MAIN WORKSPACE ---

# --- SIDEBAR (TOOLS & METRICS) ---
with st.sidebar:
    st.markdown("<h3 style='color: #e2e8f0; font-size: 1.2rem; margin-bottom: 20px;'>Dashboard</h3>", unsafe_allow_html=True)
    
    # Custom Metric Cards
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Indexed Models</div>
            <div class="metric-value">24 <span class="metric-delta">↑ 2</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Graph Accuracy</div>
            <div class="metric-value">98.5% <span class="metric-delta">Stable</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔄 Force Graph Sync"):
        with st.spinner("Synchronizing Knowledge Graph..."):
            time.sleep(1.5)
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            time.sleep(0.5)
            st.success("Vector DB Synchronized.")
            progress.empty()
                
    st.markdown("<hr style='border-color: #1e293b;'>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #cbd5e1; font-size: 1rem;'>Quick Workflows</h4>", unsafe_allow_html=True)
    quick_action = st.radio(
        "Run playbook:",
        ["Select Action...", "Analyze Kubernetes Pod YAML", "Optimize Docker Build Cache", "Audit Terraform Security"],
        index=0,
        label_visibility="collapsed"
    )

# --- CHAT AREA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome. I am connected to your enterprise knowledge graph (`data/`). How can I assist with your deployments today?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Quick Actions
if quick_action != "Select Action..." and ("last_action" not in st.session_state or st.session_state.last_action != quick_action):
    st.session_state.last_action = quick_action
    st.session_state.messages.append({"role": "user", "content": quick_action})
    st.rerun()

# User Input
if prompt := st.chat_input("Ask a question about your infrastructure..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Analyzing context..."):
            # Simulation response styled like the image
            time.sleep(1)
            raw_answer = f"""Here is an analysis based on your query: **{prompt}**.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: optimized-app
spec:
  containers:
  - name: app-container
    image: myrepo/app:latest
    resources:
      limits:
        memory: "256Mi"
        cpu: "500m"
```

*In a live deployment, this response would be generated by the fine-tuned LLM processing your private documents.*"""
            
            # Typewriter Effect
            for chunk in raw_answer.split():
                full_response += chunk + " "
                time.sleep(0.04)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
