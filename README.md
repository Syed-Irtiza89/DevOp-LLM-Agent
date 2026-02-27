# 🚀 DevOps LLM Agent 

An open-source, locally hosted Large Language Model (LLM) agent specialized in DevOps tasks. Built using **FastAPI**, **Streamlit**, **LangChain**, and **Ollama**, this agent leverages Retrieval-Augmented Generation (RAG) to provide intelligent answers based on your company's private infrastructure documentation, scripts, and policies.

## ✨ Features
- **Privacy-First (Air-gapped AI)**: Runs entirely on your local machine or private cloud. Your code and proprietary documentation never leave your network.
- **DevOps Expertise**: Designed to assist with Docker, Kubernetes, Terraform, CI/CD pipelines, and general cloud architecture.
- **RAG-Powered Knowledge Base**: Upload your company-specific `.md`, `.txt`, or code files into the `data/` directory, and the agent will instantly learn your internal workflows.
- **SaaS Ready**: Fully containerized using Docker Compose for 1-click enterprise deployments.
- **Premium Web Interface**: A sleek, dark-mode dashboard built with Streamlit.

## 🛠️ Technology Stack
- **Backend**: FastAPI, Python 3.10
- **Frontend**: Streamlit
- **AI & RAG**: LangChain, ChromaDB (Vector Store), BAAI/bge-small-en-v1.5 (Embeddings)
- **Model Execution**: Ollama (supports GGUF quantization like Llama 3 / Qwen 2.5)
- **Orchestration**: Docker & Docker Compose
- **Training**: Unsloth (Fine-tuning notebooks included)

## 🚀 Getting Started (Local Preview)

If you don't have Ollama or a GPU set up yet, you can run the UI in **Preview Mode**.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/devops-llm-agent.git
   cd devops-llm-agent
   ```

2. **Run the local preview script (Windows):**
   ```cmd
   double-click run_preview.bat
   ```
   *(This will start both the FastAPI backend and Streamlit frontend. The app will be available at `http://localhost:8501`)*

## 📦 Full Enterprise Deployment (Docker)

To deploy the production-ready stack with a live model:

1. **Prerequisites**: Install Docker and Docker Compose.
2. **Download Model**: Ensure Ollama is running and a model is pulled (e.g., `ollama pull llama3`).
3. **Start the Stack**:
   ```bash
   docker-compose up --build -d
   ```
4. **Access the Application**:
   - Frontend: `http://localhost:8501`
   - Backend API Docs: `http://localhost:8000/docs`

## 📚 Adding Custom Knowledge
Drop your company documents, markdown files, or code snippets into the `data/` folder. Click **"Refresh Knowledge Base"** in the UI sidebar, and the agent will immediately contextualize its answers based on your new files.

## 📄 License
MIT License
