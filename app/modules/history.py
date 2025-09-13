from typing import List
from .message import Message
import os
from datetime import datetime
from collections import Counter

class History:
    def __init__(self, log_filename: str = "chat_log.txt"):
        self.session_messages: List[Message] = []
        self.log_filename = log_filename

    def add_message(self, message: Message):
        self.session_messages.append(message)

    def show_session(self):
        print("\n--- Conversation History ---")
        if not self.session_messages:
            print("(No messages in this session)")
            return
        for msg in self.session_messages:
            time_str = msg.timestamp.strftime("%H:%M:%S")
            print(f"[{time_str}] {msg.sender}: {msg.text}")
        print("---------------------------\n")

    def show_last_interactions(self):
        print("\n--- Últimas 5 Interações ---")
        if hasattr(self, 'last_interactions') and self.last_interactions:
            for line in self.last_interactions:
                print(line.strip())
        else:
            print("(Nenhum histórico anterior encontrado)")
        print("-----------------------------\n")

    def save_session(self):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"\n--- Session started {self.session_messages[0].timestamp.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            for msg in self.session_messages:
                time_str = msg.timestamp.strftime("%H:%M:%S")
                f.write(f"[{time_str}] {msg.sender}: {msg.text}\n")
            f.write("--- End of Session ---\n")
        print(f"(History saved in '{self.log_filename}')")

    def load_last_interactions(self, num_interactions: int = 6):
        try:
            with open(self.log_filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                self.last_interactions = lines[-num_interactions:]
        except FileNotFoundError:
            self.last_interactions = []
        except Exception as e:
            print(f"Erro ao carregar o histórico: {e}")
            self.last_interactions = []

    def get_session_stats(self) -> dict:
        if not self.session_messages:
            return {
                "user_interactions": 0,
                "most_frequent_question": "Nenhuma pergunta feita."
            }

        user_messages = [
            msg.text.lower() for msg in self.session_messages if msg.sender.lower() != 'academico' 
            and msg.sender.lower() != 'gamificado' and msg.sender.lower() != 'acessivel'
        ]

        if not user_messages:
            return {
                "user_interactions": 0,
                "most_frequent_question": "Nenhuma pergunta feita."
            }

        question_counts = Counter(user_messages)
        most_common = question_counts.most_common(1)[0]

        stats = {
            "user_interactions": len(user_messages),
            "most_frequent_question": f"'{most_common[0]}' (feita {most_common[1]} vez(es))"
        }
        
        return stats
