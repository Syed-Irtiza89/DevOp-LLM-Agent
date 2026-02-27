@echo off
echo Starting DevOps LLM Agent Preview...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python.
    pause
    exit /b
)

:: Install basic requirements for preview
echo Installing requirements for preview...
pip install fastapi uvicorn streamlit requests langchain langchain_community chromadb sentence-transformers

:: Start Backend in a new window
echo Starting Backend...
start cmd /k "cd backend && python main.py"

:: Start Frontend
echo Starting Frontend UI...
cd frontend && streamlit run app.py

pause
