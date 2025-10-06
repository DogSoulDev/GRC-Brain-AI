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
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python main.py
   ```

## Features
- Local AI assistant for GRC, cybersecurity, legal, risk, and compliance queries
- Modern, professional dark GUI (Copilot VS Code style)
- Secure, private, and offline operation
- RAG (Retrieval Augmented Generation) with ChromaDB and official documents
- English only: all information, spellchecking, and resources are in English
- Easy document upload and knowledge expansion

## Architecture
- Modular, hexagonal, clean codebase
- SOLID, DRY, and KISS principles

## Project Structure
- `main.py`: Entry point
- `src/gui/app.py`: Main application window and loader animation
- `src/gui/tabs/chat_tab.py`: Chat interface
- `src/ai_core/llm_client.py`: Ollama LLM client
- `src/ai_core/rag_system.py`: RAG integration
- `src/utils/spellcheck_utils.py`: English spellchecking utilities
- `official_docs/`: Preloaded official documents and links

## Official Resources
All legal, regulatory, and technical information is preloaded from official sources. See `official_docs/` and `official_docs/official_links.txt` for documents and links. All resources are in English and indicate the country of reference.

## License
This software is open source, but commercial use or sale is prohibited. Attribution to DogSoulDev and https://dogsouldev.github.io/Web/ is required.