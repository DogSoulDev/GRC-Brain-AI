"""
FeedbackManager - Feedback management and self-improvement for GRC Brain AI
"""
import os
import json
from datetime import datetime

class FeedbackManager:
    def __init__(self, log_path="feedback_log.json"):
        self.log_path = log_path
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_feedback(self, question, answer, rating, comment=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "rating": rating,
            "comment": comment or ""
        }
        with open(self.log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.append(entry)
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_feedback(self):
        with open(self.log_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_stats(self):
        feedback = self.get_feedback()
        total = len(feedback)
        avg_rating = sum(f["rating"] for f in feedback) / total if total else 0
        return {"total": total, "avg_rating": avg_rating}
