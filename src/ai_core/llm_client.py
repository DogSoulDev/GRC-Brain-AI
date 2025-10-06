"""
GRCBrainLLM - LLM Client for Ollama
"""
from langchain_ollama import OllamaLLM
import requests
import os
import shutil

class GRCBrainLLM:
    def _is_greeting_or_conversational(self, query):
        # Simple intent detection using keywords only (compatible with Python 3.13)
        greetings = ["hello", "hi", "hey", "how are you", "good morning", "good afternoon", "good evening", "what's up", "yo", "sup"]
        query_lower = query.lower()
        for g in greetings:
            if g in query_lower:
                return True
        # If query is short and contains only conversational words
        if len(query.split()) <= 4:
            return True
        return False
    def __init__(self, host="http://localhost:11434", model="llama3:8b"):
        self.host = host
        self.model = model
        self.llm = None
        self.ollama_path = self._find_ollama_path()
        if not self.ollama_path:
            self.llm = None
            self.error = "[ERROR] Ollama is not installed. Download from https://ollama.com/download and ensure it's in your PATH."
        else:
            try:
                # Verificar si Ollama está activo
                response = requests.get(f"{self.host}/api/tags", timeout=5)
                if response.status_code != 200:
                    self.llm = None
                    self.error = "[ERROR] Ollama service is not running. Start Ollama with 'ollama serve' in terminal."
                else:
                    tags = response.json()
                    available = [m['name'] for m in tags.get('models', [])]
                    if self.model not in available:
                        self.llm = None
                        self.error = f"[ERROR] Model '{self.model}' not found. Run 'ollama pull {self.model}' in terminal. Available: {available}"
                    else:
                        self.llm = OllamaLLM(base_url=self.host, model=self.model)
                        self.error = None
            except Exception:
                self.llm = None
                self.error = "[ERROR] Could not connect to Ollama. Ensure Ollama is running and accessible."

    def _find_ollama_path(self):
        # Detectar Ollama en PATH o ruta estándar de Windows
        if shutil.which("ollama"):
            return shutil.which("ollama")
        win_path = os.path.expanduser(r"C:\Users\dogso\AppData\Local\Programs\Ollama\ollama.exe")
        if os.path.exists(win_path):
            return win_path
        return None

    def ask(self, query: str, context=None, language="auto") -> str:
        if not self.llm:
            return self.error or "[ERROR] No local LLM available. Check Ollama installation."
        try:
            # Use spaCy for intent detection
            is_greeting = self._is_greeting_or_conversational(query)
            # Language selection
            if language == "es":
                lang_instruction = "Answer in Spanish, referencing official laws and standards from Spain and the USA."
            elif language == "en":
                lang_instruction = "Answer in English, referencing official frameworks and laws from the USA, EU, and international sources."
            else:
                lang_instruction = "Always answer in English, referencing official frameworks and laws from the USA, EU, and international sources."
            # Flexible prompt: skip instructions/context for greetings
            if is_greeting:
                prompt = query
            else:
                context_str = ""
                if context:
                    if isinstance(context, list):
                        context_str = "\nContext:\n" + "\n---\n".join([c["content"] for c in context])
                    else:
                        context_str = f"\nContext:\n{context}"
                prompt = f"{lang_instruction}\nQuestion: {query}{context_str}"
            # Query log for traceability
            self._log_query(query, context, language)
            return self.llm.invoke(prompt)
        except Exception as e:
            return f"[ERROR] Could not get response from LLM: {e}"

    def _log_query(self, query, context, language):
        log_path = "llm_query_log.json"
        import json
        from datetime import datetime
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "context": context,
            "language": language
        }
        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f)
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.append(entry)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
