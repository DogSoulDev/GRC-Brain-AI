"""
GRCBrainApp - Main Application Window
"""
import customtkinter as ctk
from src.gui.tabs.chat_tab import ChatTab

class GRCBrainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Brain")
        self.geometry("900x600")
        self.configure(bg="#181818")
        self.loader_frame = None
        self.after(100, self._show_loader)

    def _show_loader(self):
        import time
        import threading
        import os
        from PIL import Image, ImageTk
        self.loader_frame = ctk.CTkFrame(self, fg_color="#181818")
        self.loader_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        win_w, win_h = self.winfo_width(), self.winfo_height()
        if win_w < 100 or win_h < 100:
            win_w, win_h = 900, 600
        self.anim_canvas = ctk.CTkCanvas(self.loader_frame, width=win_w, height=win_h, bg="#181818", highlightthickness=0)
        self.anim_canvas.pack(fill="both", expand=True)
        # Load and resize background JPEG
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../img'))
        bg_path = os.path.join(img_dir, '2.jpeg')
        if not os.path.exists(bg_path):
            bg_path = os.path.join(img_dir, '2.jpg')
        if not os.path.exists(bg_path):
            raise FileNotFoundError(f'No se encontró la imagen de fondo: {bg_path}')
        bg_img = Image.open(bg_path).resize((win_w, win_h), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_img)
        if not hasattr(self, '_loader_images'):
            self._loader_images = []
        self._loader_images.append(bg_photo)
        self.anim_canvas.create_image(0, 0, anchor="nw", image=bg_photo)
        # Movie-style rotating intro text
        # Movie-style rotating intro text, all in one phrase, moved left
        main_text_y = win_h // 2 - 200
        main_x = win_w // 2 - 220  # Move further left
        main_font = ('Arial Narrow', 32, 'bold')
        loading_bar_color = '#ff9900'
        rotating_words = [
            ('secure.', loading_bar_color),
            ('compliant.', loading_bar_color),
            ('legal.', loading_bar_color),
            ('modern.', loading_bar_color),
            ('intelligent.', loading_bar_color),
        ]
        self._rotating_word_idx = 0
        rotating_font = ('Arial Narrow', 32, 'bold')
        # Store text item ids to clear them
        self._main_text_id = None
        self._rotating_text_id = None
        def update_rotating_word():
            if not hasattr(self, 'anim_canvas') or not self.anim_canvas.winfo_exists():
                return
            # Delete previous text items if they exist
            if self._main_text_id:
                self.anim_canvas.delete(self._main_text_id)
            if self._rotating_text_id:
                self.anim_canvas.delete(self._rotating_text_id)
            word, color = rotating_words[self._rotating_word_idx]
            self._main_text_id = self.anim_canvas.create_text(
                main_x, main_text_y,
                text='GRC Brain is ',
                font=main_font,
                fill='white',
                anchor='w'
            )

            bbox = self.anim_canvas.bbox(self._main_text_id)
            if bbox:
                static_text_width = bbox[2] - bbox[0]
            else:
                static_text_width = 320  # fallback

            self._rotating_text_id = self.anim_canvas.create_text(
                main_x + static_text_width + 20, main_text_y,
                text=word,
                font=rotating_font,
                fill=color,
                anchor='w'
            )
            self._rotating_word_idx = (self._rotating_word_idx + 1) % len(rotating_words)
            self.after(2000, update_rotating_word)
        update_rotating_word()
        # Use new birds image for animation (5.png)
        bird_png_path = os.path.join(img_dir, '5.png')
        if os.path.exists(bird_png_path):
            bird_img = Image.open(bird_png_path).resize((80, 80), Image.Resampling.LANCZOS)
            self.bird_photos = [ImageTk.PhotoImage(bird_img.copy()) for _ in range(4)]
            self._loader_images += self.bird_photos
        else:
            self.bird_photos = []
        # Animated birds overlay (3.svg above text, centered horizontally, moving left to right)
        self._bird_ids = []
        if hasattr(self, 'bird_photos') and self.bird_photos:
            # Only 2 birds, positioned higher above the text, moving left/right
            birds_y = win_h // 2 - 160  # Higher above the text
            birds_x_positions = [win_w // 2 - 180, win_w // 2 + 180]
            self._bird_positions = birds_x_positions
            self._bird_y_positions = [birds_y, birds_y]
            self._bird_speeds = [2, -2]
            self._bird_y_speeds = [0, 0]
            self._bird_ids = []
            for i in range(len(self._bird_positions)):
                bird_id = self.anim_canvas.create_image(self._bird_positions[i], self._bird_y_positions[i], anchor='nw', image=self.bird_photos[i % len(self.bird_photos)])
                self._bird_ids.append(bird_id)
            def animate_birds():
                if not hasattr(self, 'anim_canvas') or not self.anim_canvas.winfo_exists():
                    return
                # Prevent birds from overlapping by keeping minimum distance
                min_dist = 90
                for i, bird_id in enumerate(self._bird_ids):
                    x = self._bird_positions[i] + self._bird_speeds[i]
                    y = self._bird_y_positions[i] + self._bird_y_speeds[i]
                    # Wrap horizontally
                    if x > win_w:
                        x = -80
                    if x < -80:
                        x = win_w
                    # Wrap vertically
                    if y > win_h - 80:
                        y = birds_y
                    if y < 0:
                        y = birds_y
                    # Check for overlap with other birds
                    for j in range(len(self._bird_ids)):
                        if i != j:
                            if abs(x - self._bird_positions[j]) < min_dist and abs(y - self._bird_y_positions[j]) < min_dist:
                                y += min_dist
                    self._bird_positions[i] = x
                    self._bird_y_positions[i] = y
                    try:
                        self.anim_canvas.coords(bird_id, x, y)
                    except Exception:
                        pass
                self.after(40, animate_birds)
            animate_birds()
        # Custom neon/orange loading bar (CodePen style)
        self.progress_canvas = ctk.CTkCanvas(self.loader_frame, width=320, height=32, bg="#181818", highlightthickness=0)
        self.progress_canvas.place(relx=0.5, rely=0.95, anchor="s")
        self.progress_bar_bg = self.progress_canvas.create_rectangle(10, 10, 310, 22, fill="#23272a", outline="#ff9900", width=2)
        self.progress_bar_fg = self.progress_canvas.create_rectangle(10, 10, 10, 22, fill="#ff9900", outline="", width=0)
        def animate_bar():
            for i in range(1, 301):
                try:
                    if hasattr(self, 'progress_canvas') and self.progress_canvas.winfo_exists():
                        self.progress_canvas.coords(self.progress_bar_fg, 10, 10, 10+i, 22)
                        self.progress_canvas.update()
                    else:
                        break
                except Exception:
                    break
                time.sleep(0.01)
        threading.Thread(target=animate_bar, daemon=True).start()
        def animate_and_load():
            from src.ai_core.llm_client import GRCBrainLLM
            from src.ai_core.rag_system import GRCRAGSystem
            llm_ready = False
            rag_ready = False
            llm_check = None
            rag_check = None
            for i in range(30):
                time.sleep(0.07)
                if i == 5:
                    llm_check = GRCBrainLLM()
                    llm_ready = llm_check.llm is not None
                if i == 15:
                    rag_check = GRCRAGSystem()
                    rag_ready = True
            while not llm_ready:
                time.sleep(0.2)
                llm_check = GRCBrainLLM()
            time.sleep(0.2)
            self.after(0, self._finish_loader)
        def _finish_loader():
            if self.loader_frame:
                self.loader_frame.destroy()
            self._setup_ui()
        self._finish_loader = _finish_loader
        threading.Thread(target=animate_and_load, daemon=True).start()
    def _setup_ui(self):
        self.chat_tab = ChatTab(self)
        self.chat_tab.pack(fill="both", expand=True)
