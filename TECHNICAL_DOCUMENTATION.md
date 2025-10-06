

# DsD GRC AI - Technical Documentation

![Intro Animation](src/img/Intro.png)
![AI Main View](src/img/Base.png)

## Overview
DsD GRC AI is a local desktop assistant for compliance, risk, legal, and cybersecurity queries. It uses local LLMs (Ollama, Llama 3), RAG (ChromaDB), and a modern CustomTkinter GUI inspired by Copilot in VS Code.

## AI Models and Engines
### Ollama (Llama 3)
- Runs advanced LLMs locally, no cloud required
- Full privacy and easy integration with Python/LangChain
- Download: https://ollama.com/download
- Docs: https://ollama.com/docs
- Python Library: https://github.com/ollama/ollama-python

### ChromaDB and LangChain RAG
- Enables the AI to learn from legal and regulatory documents
- ChromaDB stores texts and converts them to embeddings for contextual search
- Uses `sentence-transformers/all-MiniLM-L6-v2` (lightweight, fast, effective)
- ChromaDB: https://docs.trychroma.com/
- LangChain: https://python.langchain.com/docs/

## Architecture
- Modular, hexagonal, clean architecture
- SOLID, DRY, and KISS principles
- CustomTkinter GUI (Copilot VS Code style, professional dark)
- Pagination and result selector for large datasets
- Visual warnings for large queries and documents
- Easy document upload and knowledge expansion

## Requirements
- Python 3.11+
- Ollama (Llama 3)
- ChromaDB
- CustomTkinter
- All dependencies in `requirements.txt`

## Usage
1. Install Python 3.11 or higher
2. Install Ollama and pull the Llama 3 model
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

## Knowledge Base Expansion
- Add TXT, PDF, DOCX, XLSX, CSV, HTML, Markdown, or JSON files to `official_docs/` or use the "Add File" button in the interface
- Consult and download links in `official_docs/official_links.txt`

## Expert Usage
- The AI responds only in English and cites official sources
- History and logs show sources, country, and legal context

## License
This software is Open Source, but commercial use or sale is prohibited. Attribution to DogSoulDev and https://dogsouldev.github.io/Web/ is required.
