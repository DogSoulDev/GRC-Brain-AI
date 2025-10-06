"""
file_loader.py - Carga y procesamiento de archivos para RAG
Soporta TXT, PDF, DOCX, XLSX, CSV, HTML, Markdown, JSON
"""
import os
import pandas as pd
from bs4 import BeautifulSoup
import markdown
import json
from docx import Document as DocxDocument
from PyPDF2 import PdfReader

class FileLoader:
    @staticmethod
    def load_file(path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".txt":
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == ".pdf":
            reader = PdfReader(path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        elif ext == ".docx":
            doc = DocxDocument(path)
            return "\n".join([p.text for p in doc.paragraphs])
        elif ext == ".csv":
            df = pd.read_csv(path)
            return df.to_string()
        elif ext == ".xlsx":
            df = pd.read_excel(path)
            return df.to_string()
        elif ext == ".html":
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                return soup.get_text()
        elif ext == ".md":
            with open(path, "r", encoding="utf-8") as f:
                return markdown.markdown(f.read())
        elif ext == ".json":
            with open(path, "r", encoding="utf-8") as f:
                return json.dumps(json.load(f), indent=2)
        else:
            return None
