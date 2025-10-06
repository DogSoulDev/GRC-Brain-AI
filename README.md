# GRC Brain AI

![Intro Animation](src/img/Intro.png)
![AI Main View](src/img/Base.png)




# GRC Brain AI

GRC Brain AI is a desktop application for secure, local management and querying of official GRC (Governance, Risk, and Compliance), cybersecurity, legal, and risk information. It uses local LLMs (Ollama, Llama 3), RAG (ChromaDB), and a modern CustomTkinter GUI inspired by Copilot in VS Code.

## Quick Start
1. Clone the repository:
   ```
   git clone https://github.com/DogSoulDev/GRC-Brain-AI.git
   cd GRC-Brain-AI
   ```
2. Install Python 3.11 or higher.
3. Install Ollama and pull the Llama 3 model:
   - Download from: https://ollama.com/download
   - Run:
     ```
     ollama serve
     ollama pull llama3:8b
     ollama list
     ```
   - Confirm `llama3:8b` is available.
# GRC Brain AI

GRC Brain AI is a free, local desktop assistant for Governance, Risk, Compliance, cybersecurity, and legal queries. It runs fully offline, using open-source AI models and your own documents.

## Quick Start
1. Clone the repository:
   ```
   git clone https://github.com/DogSoulDev/GRC-Brain-AI.git
   cd GRC-Brain-AI
   ```
2. Install Python 3.13 or higher.
3. Install Ollama and pull the Llama 3 model:
   - Download from: https://ollama.com/download
   - Run:
     ```
     ollama serve
     ollama pull llama3:8b
     ollama list
     ```
   - Confirm `llama3:8b` is available.
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python main.py
   ```

## Main Features
- Local, private AI chat for GRC, cybersecurity, legal, and risk topics
- Modern, easy-to-use interface
- RAG (Retrieval Augmented Generation) with ChromaDB and your own documents
- No cloud, no tracking, no external API keys needed
- Add TXT, PDF, DOCX, XLSX, CSV, HTML, Markdown, or JSON files to expand knowledge

## How to Use
- Type your question in English and get instant answers
- Upload documents to make the AI smarter
- All sources and knowledge are stored locally

## Requirements
- Python 3.13+
- Ollama (Llama 3)
- ChromaDB
- CustomTkinter
- All dependencies in `requirements.txt`

## License
Open source for personal and educational use. Attribution to DogSoulDev and https://dogsouldev.github.io/Web/ is required.