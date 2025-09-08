from typing import List
from .message import Message

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

    def save_session(self):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"\n--- Session started {self.session_messages[0].timestamp.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            for msg in self.session_messages:
                time_str = msg.timestamp.strftime("%H:%M:%S")
                f.write(f"[{time_str}] {msg.sender}: {msg.text}\n")
            f.write("--- End of Session ---\n")
        print(f"(History saved in '{self.log_filename}')")
