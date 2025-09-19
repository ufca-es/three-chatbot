from datetime import datetime

# define uma mensagem da conversa
class Message:
    
    def __init__(self, sender: str, text: str):
        self.sender = sender
        self.text = text
        self.timestamp = datetime.now()

    # retorna uma mensagem formatada
    def __repr__(self) -> str:
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"Message(sender='{self.sender}', text='{self.text}', timestamp='{time_str}')"
