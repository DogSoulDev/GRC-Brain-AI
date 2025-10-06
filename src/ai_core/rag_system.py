"""
GRCRAGSystem - RAG and ChromaDB Integration
"""
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

class GRCRAGSystem:
    def _async_similarity_search(self, queries, k=3):
        """
        Perform batched/async semantic search for multiple queries using concurrent.futures.
        """
        import concurrent.futures
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_query = {executor.submit(self.vector_db.similarity_search, q, k): q for q in queries}
            for future in concurrent.futures.as_completed(future_to_query):
                res = future.result()
                results.append(res)
        return results
    def _chunk_text(self, text, chunk_size=1000):
        """
        Split text into chunks for large document support in RAG.
        """
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    def __init__(self, db_path="chromadb"):
        self.db_path = db_path
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-cos-v1")
        self.vector_db = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)

    def add_document(self, path: str):
        # Supports multiple formats and chunks large files
        from src.ai_core.file_loader import FileLoader
        if not os.path.isfile(path):
            return False
        content = FileLoader.load_file(path)
        if not content:
            return False
        from langchain_core.documents import Document
        chunks = self._chunk_text(content, chunk_size=1200)
        docs = [Document(page_content=chunk, metadata={"source": os.path.basename(path)}) for chunk in chunks]
        self.vector_db.add_documents(docs)
        return True
    def _cache_search(self):
        """
        Simple in-memory cache for semantic search queries.
        """
        if not hasattr(self, '_search_cache'):
            self._search_cache = {}
        return self._search_cache
    def add_chat_to_db(self, question, answer):
        # Incremental learning: add each relevant conversation
        from langchain_core.documents import Document
        doc = Document(page_content=f"Question: {question}\nAnswer: {answer}", metadata={"source": "chat"})
        self.vector_db.add_documents([doc])
        return True
    def clean_database(self):
        # Clean the local database
        self.vector_db.delete_collection()
        return True

    def search(self, query: str, k=3, page=1, batch_queries=None):
        """
        Perform semantic search with pagination, chunking, caching, and async/batched search for best performance.
        If batch_queries is provided, run async search for all queries and return combined results.
        """
        cache = self._cache_search()
        if batch_queries:
            # Batched/async search for multiple queries
            batch_results = self._async_similarity_search(batch_queries, k=k)
            combined = []
            for res in batch_results:
                combined.extend(res)
            return [{"content": r.page_content, "metadata": r.metadata} for r in combined]
        cache_key = f"{query}|{k}|{page}"
        if cache_key in cache:
            results = cache[cache_key]
        else:
            offset = (page - 1) * k
            results = self.vector_db.similarity_search(query, k=k+offset)
            cache[cache_key] = results
        paged_results = results[offset:offset+k]
        if len(results) > 100:
            print("[WARNING] The database is large. Use pagination and limit k for best performance.")
        return [{"content": r.page_content, "metadata": r.metadata} for r in paged_results]
