



# GRC Brain AI - Technical Documentation

## What is GRC Brain AI?
GRC Brain AI is a free, offline desktop assistant for Governance, Risk, Compliance, cybersecurity, and legal questions. It uses open-source AI models and lets you expand its knowledge with your own documents.

## How does it work?
- Uses Ollama (Llama 3) for local AI chat
- Uses ChromaDB for fast document search and retrieval
- Modern interface built with CustomTkinter
- No cloud, no external API keys, no tracking

## Installation & Usage
1. Install Python 3.13 or higher
2. Install Ollama and pull the Llama 3 model
	- Download Ollama: https://ollama.com/download
	- Run:
	  ```
	  ollama serve
	  ollama pull llama3:8b
	  ollama list
	  ```
3. Install dependencies:
	```
	pip install -r requirements.txt
	```
4. Run the app:
	```
	python main.py
	```

## How to expand the AI's knowledge
- Upload TXT, PDF, DOCX, XLSX, CSV, HTML, Markdown, or JSON files using the "Add Document" button
- All files are stored and processed locally

## For users
- Ask questions in English
- Upload documents to make the AI smarter
- All answers and sources are local and private

## Requirements
- Python 3.13+
- Ollama (Llama 3)
- ChromaDB
- CustomTkinter
- All dependencies in `requirements.txt`

## License
Open source for personal and educational use. Attribution to DogSoulDev and https://dogsouldev.github.io/Web/ is required.
