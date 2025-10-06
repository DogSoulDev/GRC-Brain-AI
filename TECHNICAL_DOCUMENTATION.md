


# GRC Brain AI - Technical Documentation

## Overview
GRC Brain AI is a local desktop assistant for compliance, risk, legal, and cybersecurity queries. It uses local LLMs (Ollama, Llama 3), RAG (ChromaDB), and a modern CustomTkinter GUI inspired by Copilot in VS Code.

## AI Models and Engines
### Ollama (Llama 3)
- Runs advanced LLMs locally, no cloud required
- Full privacy and easy integration with Python/LangChain
- Download: https://ollama.com/download

### ChromaDB and LangChain RAG
- Enables the AI to learn from legal and regulatory documents
- ChromaDB stores texts and converts them to embeddings for contextual search
- Uses `sentence-transformers/multi-qa-mpnet-base-cos-v1` for embeddings

## Architecture
- Modular, hexagonal, clean codebase
- SOLID, DRY, and KISS principles
- CustomTkinter GUI (Copilot VS Code style)

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
- Add TXT, PDF, DOCX, XLSX, CSV, HTML, Markdown, or JSON files using the "Add Document" button or place in `official_docs/`
- Consult and download links in `official_docs/official_links.txt`

## Expert Usage
- The AI responds only in English and cites official sources
- History and logs show sources, country, and legal context

## License
This software is Open Source, but commercial use or sale is prohibited. Attribution to DogSoulDev and https://dogsouldev.github.io/Web/ is required.
