from .message import Message

# personalidades do bot

class Personality:
    """Personalidade padrão, extremamente básica."""

    def __init__(self, name: str = "academico"):
        self.name = name

    def reply(self, text: str) -> Message:
        new_text = text
        return Message(sender=self.name, text=new_text)
    
    def get_greeting(self) -> Message:
        return Message(sender=self.name, text="Olá!")

    def get_farewell(self) -> Message:
        return Message(sender=self.name, text="Tchau!")
    
    def set_personality(self, action: str):
        if action == "set_academico":
            self.name = "academico"
        elif action == "set_acessivel":
            self.name = "acessivel"
        elif action == "set_gamificado":
            self.name = "gamificado"
        else:
            self.name = "academico"
