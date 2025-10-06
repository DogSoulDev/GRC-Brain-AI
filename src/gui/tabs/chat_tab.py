"""
ChatTab - Minimalist Professional Chat Interface for GRC Brain AI
"""
import customtkinter as ctk
import threading
from src.ai_core.llm_client import GRCBrainLLM
from src.ai_core.rag_system import GRCRAGSystem
from src.utils.feedback import FeedbackManager
from tkinter import filedialog, messagebox

class ChatTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#222")
        self.llm = GRCBrainLLM()
        self.rag = GRCRAGSystem()
        self.feedback = FeedbackManager()
        self.last_question = None
        self.last_answer = None
        self.feedback_btn = None
        self.history = []
        self.k_results = 3
        self.page = 1
        self.uploaded_files = []  # Track uploaded files: [{'filename': ..., 'path': ..., 'date': ...}]
        self._setup_ui()

    def _setup_ui(self):
        # Top bar with settings icon
        top_bar = ctk.CTkFrame(self, fg_color="#181818", height=54)
        top_bar.pack(fill="x", side="top")
        ctk.CTkLabel(top_bar, text="Brain", font=("JetBrains Mono", 24, "bold"), text_color="#ff9800").pack(side="left", padx=24)
        settings_icon = ctk.CTkButton(top_bar, text="⚙️", command=self._open_settings, fg_color="#23272a", text_color="#ff9800", width=40, height=40, font=("JetBrains Mono", 20), corner_radius=20)
        settings_icon.pack(side="right", padx=16)

        # Central chat panel
        chat_panel = ctk.CTkFrame(self, fg_color="#181818", corner_radius=18)
        chat_panel.pack(fill="both", expand=True, padx=0, pady=0)
        self.chat_display = ctk.CTkTextbox(chat_panel, font=("JetBrains Mono", 17), fg_color="#23272a", text_color="#fffde7", border_color="#ff9800", border_width=2)
        self.chat_display.pack(fill="both", expand=True, padx=32, pady=(32,12))
        self.chat_display._textbox.config(wrap="word")
        self.chat_display._textbox.tag_configure("user", background="#212121", foreground="#ff9800", justify="right", lmargin1=60, lmargin2=60, rmargin=10, font=("JetBrains Mono", 17, "bold"))
        self.chat_display._textbox.tag_configure("ai", background="#23272a", foreground="#fffde7", justify="left", lmargin1=10, lmargin2=10, rmargin=60, font=("JetBrains Mono", 17))

        # Info bar for spellcheck/suggestions/intent
        self.info_bar = ctk.CTkLabel(chat_panel, text="", font=("Segoe UI", 14), fg_color="#181818", text_color="#ff9800", anchor="w")
        self.info_bar.pack(fill="x", padx=32, pady=(0,4))

        # Input and actions
        input_frame = ctk.CTkFrame(chat_panel, fg_color="#181818")
        input_frame.pack(fill="x", padx=32, pady=(0,24))
        self.input_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message...", font=("JetBrains Mono", 16), fg_color="#23272a", text_color="#fffde7", border_color="#ff9800", border_width=2)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0,12), pady=0)
        self.input_entry.bind("<Return>", lambda event: self._on_ask())
        ask_btn = ctk.CTkButton(input_frame, text="Send", command=self._on_ask, fg_color="#ff9800", text_color="#23272a", font=("JetBrains Mono", 16, "bold"), corner_radius=18)
        ask_btn.pack(side="left", padx=(0,12))
        self.upload_btn = ctk.CTkButton(input_frame, text="📄 Add Document", command=self._on_upload, fg_color="#388e3c", text_color="#fffde7", font=("JetBrains Mono", 16), corner_radius=18)
        self.upload_btn.pack(side="left", padx=(0,8))
        clear_btn = ctk.CTkButton(input_frame, text="🧹 Clear Screen", command=self._clear_chat, fg_color="#23272a", text_color="#ff9800", font=("JetBrains Mono", 16), corner_radius=18)
        clear_btn.pack(side="left", padx=(0,8))

        # GitHub icon button (bottom right)
        import webbrowser
        web_btn = ctk.CTkButton(input_frame, text="🌐", width=36, height=36, fg_color="#181818", font=("Segoe UI", 18), command=lambda: webbrowser.open_new_tab("https://dogsouldev.github.io/Web/"))
        web_btn.pack(side="right", padx=(8,0), pady=(24,0))

        # Footer: model selector
        footer = ctk.CTkFrame(self, fg_color="#181818", height=40)
        footer.pack(fill="x", side="bottom")
        ctk.CTkLabel(footer, text="Model:", font=("Segoe UI", 13), text_color="#ff9800").pack(side="left", padx=(24,4))
        self.model_var = ctk.StringVar(value="Llama 3 (Ollama)")
        self.model_selector = ctk.CTkOptionMenu(footer, variable=self.model_var, values=["Llama 3 (Ollama)", "Mistral", "Phi-3"], command=self._on_model_change, fg_color="#23272a", text_color="#ff9800", font=("Segoe UI", 13))
        self.model_selector.pack(side="left", padx=(0,24))

        # Spellcheck/intent feedback block (fixed)
        info = ""
        # Example: suggestions = {"word": ["suggestion1", "suggestion2"]}
        suggestions = getattr(self, "spell_suggestions", {})
        for word, sugg in suggestions.items():
            info += f"💡 Suggestions for '{word}': {', '.join(sugg)}  "
        matched_phrases = getattr(self, "matched_phrases", [])
        if matched_phrases:
            info += f"🧠 Intent: {', '.join(matched_phrases)}  "
        self.info_bar.configure(text=info)

    def _clear_chat(self):
        self.chat_display.delete("1.0", "end")
        self.info_bar.configure(text="🧹 Screen cleared.")
        import threading
        def clear_info():
            import time
            time.sleep(2)
            self.info_bar.configure(text="")
        threading.Thread(target=clear_info, daemon=True).start()

    def _show_logs(self):
        import os, json
        log_path = os.path.join(os.getcwd(), "llm_query_log.json")
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                try:
                    log_entries = json.load(f)
                except Exception as e:
                    messagebox.showerror("Logs & Usage Stats", f"Error reading log file: {e}")
                    return
            # Build readable table
            table = "Timestamp        | Query         | Context Summary\n" + "-"*60 + "\n"
            for entry in log_entries[:30]:
                ts = entry.get("timestamp", "")[:19]
                q = entry.get("query", "")[:20]
                ctxs = entry.get("context", [])
                ctx_summary = ", ".join([c.get("content", "")[:40].replace("\n", " ") for c in ctxs])
                if len(ctx_summary) > 60:
                    ctx_summary = ctx_summary[:57] + "..."
                table += f"{ts:<18} | {q:<13} | {ctx_summary}\n"
            messagebox.showinfo("Logs & Usage Stats", table + "\n(Showing latest 30 entries)")
        else:
            messagebox.showinfo("Logs & Usage Stats", "No logs found.")

    def _open_privacy_controls(self):
        win = ctk.CTkToplevel(self)
        win.title("Privacy Controls")
        win.geometry("400x220")
        win.configure(bg="#23272a")
        ctk.CTkLabel(win, text="Privacy Controls", font=("Segoe UI", 18, "bold"), text_color="#ff9800", bg_color="#23272a").pack(pady=(18,8))
        ctk.CTkLabel(win, text="Data retention, logging, and privacy settings will be available here.", font=("Segoe UI", 14), text_color="#fff", bg_color="#23272a").pack(pady=(8,2))
        # Add real privacy options here as needed

    def _open_feedback(self):
        win = ctk.CTkToplevel(self)
        win.title("Feedback & Improvement")
        win.geometry("400x260")
        win.configure(bg="#23272a")
        ctk.CTkLabel(win, text="Feedback & Improvement", font=("Segoe UI", 18, "bold"), text_color="#ff9800", bg_color="#23272a").pack(pady=(18,8))
        ctk.CTkLabel(win, text="Submit feedback or suggestions to improve the AI.", font=("Segoe UI", 14), text_color="#fff", bg_color="#23272a").pack(pady=(8,2))
        feedback_entry = ctk.CTkEntry(win, placeholder_text="Your feedback...", font=("Segoe UI", 14), fg_color="#23272a", text_color="#fffde7", border_color="#ff9800", border_width=2)
        feedback_entry.pack(fill="x", padx=24, pady=(8,8))
        rating_var = ctk.IntVar(value=5)
        ctk.CTkLabel(win, text="Rating (1-5):", font=("Segoe UI", 13), text_color="#ff9800", bg_color="#23272a").pack(pady=(2,2))
        rating_entry = ctk.CTkEntry(win, textvariable=rating_var, font=("Segoe UI", 13), fg_color="#23272a", text_color="#fffde7", border_color="#ff9800", border_width=2)
        rating_entry.pack(fill="x", padx=24, pady=(2,8))
        def submit_feedback():
            feedback = feedback_entry.get()
            rating = rating_var.get()
            if feedback.strip():
                self.feedback.add_feedback(self.last_question or "", self.last_answer or "", rating, feedback)
                messagebox.showinfo("Feedback", "Thank you for your feedback!")
                win.destroy()
            else:
                messagebox.showwarning("Feedback", "Please enter feedback before submitting.")
        submit_btn = ctk.CTkButton(win, text="Submit", command=submit_feedback, fg_color="#ff9800", text_color="#23272a", font=("Segoe UI", 15), corner_radius=18)
        submit_btn.pack(pady=(2,8))

    def _open_export_import_kb(self):
        win = ctk.CTkToplevel(self)
        win.title("Export / Import Knowledge Base")
        win.geometry("400x320")
        win.configure(bg="#23272a")
        ctk.CTkLabel(win, text="Export / Import Knowledge Base", font=("Segoe UI", 18, "bold"), text_color="#ff9800", bg_color="#23272a").pack(pady=(18,8))
        ctk.CTkLabel(win, text="Export current knowledge base to file:", font=("Segoe UI", 14), text_color="#fff", bg_color="#23272a").pack(pady=(8,2))
        export_btn = ctk.CTkButton(win, text="Export to JSON", command=self._export_kb, fg_color="#23272a", text_color="#ff9800", font=("Segoe UI", 15), corner_radius=18)
        export_btn.pack(pady=(2,8))
        ctk.CTkLabel(win, text="Import knowledge base from file:", font=("Segoe UI", 14), text_color="#fff", bg_color="#23272a").pack(pady=(8,2))
        import_btn = ctk.CTkButton(win, text="Import from JSON", command=self._import_kb, fg_color="#23272a", text_color="#ff9800", font=("Segoe UI", 15), corner_radius=18)
        import_btn.pack(pady=(2,8))

    def _export_kb(self):
        # Export all documents in the vector DB to JSON
        import json
        import json
        docs = self.rag.vector_db.similarity_search("*", k=1000)
        kb_data = [{"content": d.page_content, "metadata": d.metadata} for d in docs]
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(kb_data, f, indent=2)
            messagebox.showinfo("Export Knowledge Base", f"Knowledge base exported to {file_path}")

    def _import_kb(self):
        import json
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                kb_data = json.load(f)
            # Add each document to the vector DB
            from langchain_core.documents import Document
            for doc in kb_data:
                d = Document(page_content=doc["content"], metadata=doc.get("metadata", {}))
                self.rag.vector_db.add_documents([d])
            messagebox.showinfo("Import Knowledge Base", f"Knowledge base imported from {file_path}")

    def _reset_settings(self):
        # Real reset logic: clear chat history and clean RAG database
        self.history.clear()
        self.rag.clean_database()
        self.info_bar.configure(text="Settings and data have been reset to default.")
        messagebox.showinfo("Reset Settings", "Settings and data have been reset to default.")

    # ...existing code...

    def _on_model_change(self, value):
        # Switch LLM model (stub: implement actual model switching logic)
        self.model_var.set(value)
        self.info_bar.configure(text=f"⚡ Model switched to: {value}")
        import threading
        def clear_info():
            import time
            time.sleep(3)
            self.info_bar.configure(text="")
        threading.Thread(target=clear_info, daemon=True).start()
        # TODO: reload LLM with selected model and keep RAG integration

    def _get_response(self, query):
        k = self.k_results
        page = self.page
        language = "en"
        # Check if user is requesting a PDF by name
        import re
        pdf_match = re.search(r"(?:pdf|document|archivo)\s+(de|del|de la)?\s*([\w\-.]+\.pdf)", query, re.IGNORECASE)
        if pdf_match:
            requested_pdf = pdf_match.group(2).strip().lower()
            file_info = next((f for f in self.uploaded_files if f["filename"].lower() == requested_pdf), None)
            if file_info:
                self.chat_display.insert("end", f"Brain: Aquí tienes el PDF solicitado: {file_info['filename']}\n", "ai")
                def open_file(path=file_info["path"]):
                    import os, platform
                    if platform.system() == "Windows":
                        os.startfile(path)
                    elif platform.system() == "Darwin":
                        os.system(f"open '{path}'")
                    else:
                        os.system(f"xdg-open '{path}'")
                start_idx = self.chat_display.index("end-2c")
                self.chat_display.insert("end", f"📄 {file_info['filename']}\n", "ai")
                self.chat_display._textbox.tag_add(f"file_{file_info['filename']}", start_idx, f"{start_idx} lineend")
                self.chat_display._textbox.tag_bind(f"file_{file_info['filename']}", "<Button-1>", lambda e, p=file_info["path"]: open_file(p))
                self.info_bar.configure(text="✅ PDF entregado al usuario.")
                import threading
                def clear_info():
                    import time
                    time.sleep(2)
                    self.info_bar.configure(text="")
                threading.Thread(target=clear_info, daemon=True).start()
                return
        # Normal response flow
        context = self.rag.search(query, k=k, page=page)
        context_str = "\n".join([c["content"] for c in context]) if context else ""
        sources = []
        if context:
            for c in context:
                src = c["metadata"].get("source", "") if c.get("metadata") else ""
                if src and src not in sources:
                    sources.append(src)
        sources_str = ", ".join(sources)
        full_query = f"{query}\nContext:\n{context_str}"
        response = self.llm.ask(query, context=context, language=language)
        self.last_answer = response
        self.history.append({"question": query, "answer": response, "language": language, "sources": sources_str})
        self.rag.add_chat_to_db(query, response)
        self.chat_display._textbox.tag_configure("ai", background="#23272a", foreground="#e2e8f0", justify="left", lmargin1=10, lmargin2=10, rmargin=60, font=("Inter", 16))
        # Display answer
        self.chat_display.insert("end", f"Brain: {response}\n", "ai")
        self.chat_display._textbox.see("end")
        # Only show 'Sources:' and file buttons if there are actual sources (uploaded files/links)
        if sources:
            shown = False
            for src in sources:
                file_info = next((f for f in self.uploaded_files if f["path"] == src), None)
                if file_info:
                    if not shown:
                        self.chat_display.insert("end", "Sources:\n", "ai")
                        shown = True
                    def open_file(path=src):
                        import os, platform
                        if platform.system() == "Windows":
                            os.startfile(path)
                        elif platform.system() == "Darwin":
                            os.system(f"open '{path}'")
                        else:
                            os.system(f"xdg-open '{path}'")
                    start_idx = self.chat_display.index("end-2c")
                    self.chat_display.insert("end", f"📄 {file_info['filename']}\n", "ai")
                    self.chat_display._textbox.tag_add(f"file_{file_info['filename']}", start_idx, f"{start_idx} lineend")
                    self.chat_display._textbox.tag_bind(f"file_{file_info['filename']}", "<Button-1>", lambda e, p=src: open_file(p))
        # If no sources, do not show anything extra
        # Info bar feedback for response
        self.info_bar.configure(text="✅ Response received.")
        import threading
        def clear_info():
            import time
            time.sleep(2)
            self.info_bar.configure(text="")
        threading.Thread(target=clear_info, daemon=True).start()

    def _on_upload(self):
        import os
        from datetime import datetime
        file_paths = filedialog.askopenfilenames(filetypes=[
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx"),
            ("Excel files", "*.xlsx"),
            ("CSV files", "*.csv"),
            ("HTML files", "*.html"),
            ("Markdown files", "*.md"),
            ("JSON files", "*.json")
        ])
        if file_paths:
            for file_path in file_paths:
                success = self.rag.add_document(file_path)
                if success:
                    file_info = {
                        "filename": os.path.basename(file_path),
                        "path": file_path,
                        "date": datetime.now().isoformat()
                    }
                    self.uploaded_files.append(file_info)
                    self.info_bar.configure(text=f"✅ {file_info['filename']} added to the knowledge base.")
                    import threading
                    def clear_info():
                        import time
                        time.sleep(3)
                        self.info_bar.configure(text="")
                    threading.Thread(target=clear_info, daemon=True).start()
                else:
                    self.info_bar.configure(text=f"❌ Could not upload {os.path.basename(file_path)}. Only supported formats are allowed.")
                    import threading
                    def clear_info():
                        import time
                        time.sleep(3)
                        self.info_bar.configure(text="")
                    threading.Thread(target=clear_info, daemon=True).start()

    def _open_settings(self):
        win = ctk.CTkToplevel(self)
        win.title("Settings")
        win.geometry("420x520")
        # Position window to the right of main window
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        win_x = parent_x + parent_w + 10
        win_y = parent_y + 40
        win.geometry(f"420x520+{win_x}+{win_y}")
        win.configure(bg="#23272a")
        win.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(win, text="Settings", font=("Segoe UI", 20, "bold"), text_color="#ff9800", bg_color="#23272a").grid(row=0, column=0, pady=(18,8), sticky="ew")

        # Performance Mode Section
        perf_frame = ctk.CTkFrame(win, fg_color="#23272a")
        perf_frame.grid(row=1, column=0, padx=24, pady=(8,8), sticky="ew")
        perf_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(perf_frame, text="Performance Mode", font=("Segoe UI", 16, "bold"), text_color="#ff9800", bg_color="#23272a").grid(row=0, column=0, pady=(0,6), sticky="w")
        self.performance_mode = ctk.StringVar(value="Accurate")
        def set_perf_mode(val):
            self.performance_mode.set(val)
            self.info_bar.configure(text=f"Performance mode set to: {val}")
        perf_selector = ctk.CTkOptionMenu(perf_frame, variable=self.performance_mode, values=["Fast", "Accurate"], command=set_perf_mode, fg_color="#23272a", text_color="#ff9800", font=("Segoe UI", 13))
        perf_selector.grid(row=1, column=0, pady=(2,8), sticky="ew")

        # Database Management Section
        db_frame = ctk.CTkFrame(win, fg_color="#23272a")
        db_frame.grid(row=2, column=0, padx=24, pady=(12,8), sticky="ew")
        db_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(db_frame, text="Database Management", font=("Segoe UI", 16, "bold"), text_color="#ff9800", bg_color="#23272a").grid(row=0, column=0, pady=(0,6), sticky="w")
        backup_btn = ctk.CTkButton(db_frame, text="Backup Database", fg_color="#388e3c", text_color="#fffde7", font=("Segoe UI", 15), corner_radius=18, command=self._export_kb)
        backup_btn.grid(row=1, column=0, pady=(2,8), sticky="ew")
        def confirm_delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete ALL AI data? This cannot be undone."):
                if messagebox.askyesno("Final Confirmation", "This will permanently delete all knowledge base and chat history. Proceed?"):
                    self.rag.clean_database()
                    self.history.clear()
                    self.info_bar.configure(text="All AI data deleted.")
                    messagebox.showinfo("Delete All Data", "All AI data has been deleted.")
        delete_btn = ctk.CTkButton(db_frame, text="Delete All Data", fg_color="#c62828", text_color="#fffde7", font=("Segoe UI", 15, "bold"), corner_radius=18, command=confirm_delete)
        delete_btn.grid(row=2, column=0, pady=(2,8), sticky="ew")

        # Privacy Controls Section
        privacy_frame = ctk.CTkFrame(win, fg_color="#23272a")
        privacy_frame.grid(row=3, column=0, padx=24, pady=(8,8), sticky="ew")
        privacy_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(privacy_frame, text="Privacy Controls", font=("Segoe UI", 16, "bold"), text_color="#ff9800", bg_color="#23272a").grid(row=0, column=0, pady=(0,6), sticky="w")
        self.logging_enabled = ctk.BooleanVar(value=True)
        self.data_retention_enabled = ctk.BooleanVar(value=True)
        def toggle_logging():
            self.info_bar.configure(text=f"Logging {'enabled' if self.logging_enabled.get() else 'disabled'}.")
        def toggle_retention():
            self.info_bar.configure(text=f"Data retention {'enabled' if self.data_retention_enabled.get() else 'disabled'}.")
        log_switch = ctk.CTkSwitch(privacy_frame, text="Enable Logging", variable=self.logging_enabled, command=toggle_logging, fg_color="#23272a", progress_color="#ff9800")
        log_switch.grid(row=1, column=0, pady=(2,2), sticky="w")
        retention_switch = ctk.CTkSwitch(privacy_frame, text="Enable Data Retention", variable=self.data_retention_enabled, command=toggle_retention, fg_color="#23272a", progress_color="#ff9800")
        retention_switch.grid(row=2, column=0, pady=(2,8), sticky="w")
        export_user_btn = ctk.CTkButton(privacy_frame, text="Export User Data", fg_color="#23272a", text_color="#ff9800", font=("Segoe UI", 15), corner_radius=18, command=self._show_logs)
        export_user_btn.grid(row=3, column=0, pady=(2,8), sticky="ew")

        # About/Support Section
        about_frame = ctk.CTkFrame(win, fg_color="#23272a")
        about_frame.grid(row=4, column=0, padx=24, pady=(8,8), sticky="ew")
        about_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(about_frame, text="About & Support", font=("Segoe UI", 16, "bold"), text_color="#ff9800", bg_color="#23272a").grid(row=0, column=0, pady=(0,6), sticky="w")
        ctk.CTkLabel(about_frame, text="Brain AI v1.0\nAuthor: dogsouldev\nFor support visit:", font=("Segoe UI", 13), text_color="#fff", bg_color="#23272a").grid(row=1, column=0, sticky="w")
        def open_support():
            import webbrowser
            webbrowser.open_new_tab("https://dogsouldev.github.io/Web/")
        support_btn = ctk.CTkButton(about_frame, text="Support Website", fg_color="#23272a", text_color="#ff9800", font=("Segoe UI", 15), corner_radius=18, command=open_support)
        support_btn.grid(row=2, column=0, pady=(2,8), sticky="ew")

    def _on_ask(self):
        query = self.input_entry.get()
        if not query.strip():
            self.info_bar.configure(text="Please enter a message.")
            return
        self.chat_display.insert("end", f"\nYou: {query}\n", "user")
        self.chat_display._textbox.see("end")
        self.last_question = query
        threading.Thread(target=self._get_response, args=(query,), daemon=True).start()
        self.input_entry.delete(0, "end")

