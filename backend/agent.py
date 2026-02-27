import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

# Configuration
DOCS_PATH = "../data"
DB_PATH = "./chroma_db"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = "devops-agent"

# 1. Initialize Embeddings
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def initialize_vector_db():
    """Load documents and create a vector store if it doesn't exist."""
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)
        # Create a dummy file if empty
        with open(f"{DOCS_PATH}/readme.md", "w") as f:
            f.write("# DevOps Knowledge Base\nWelcome to the company-specific DevOps docs.")

    loader = DirectoryLoader(DOCS_PATH, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings, 
        persist_directory=DB_PATH
    )
    return vectorstore

def get_qa_chain():
    """Create the RetrievalQA chain with mock failover for preview."""
    try:
        vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        llm = Ollama(base_url=OLLAMA_BASE_URL, model=MODEL_NAME)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        return qa_chain
    except Exception as e:
        # Return a Mock Chain for Preview/UI testing
        class MockChain:
            def __call__(self, inputs):
                return {
                    "result": "I am in preview mode. (Note: Ollama is not running, so this is a mock response). This agent is designed to assist you with DevOps tasks by analyzing your documents.",
                    "source_documents": []
                }
        return MockChain()

# Initialize on module load if docs exist
if os.path.exists(DOCS_PATH) and any(os.scandir(DOCS_PATH)):
    initialize_vector_db()
