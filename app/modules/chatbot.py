from .user import User
from .knowledgebase import KnowledgeBase
from .personality import Personality
from .history import History
from .message import Message

class Chatbot:
    def __init__(self, personality: Personality, knowledge_base: KnowledgeBase, history: History):
        self.personality = personality
        self.knowledge_base = knowledge_base
        self.history = history

    def process_input(self, user_message: Message) -> Message:
        self.history.add_message(user_message)
        raw_response = self.knowledge_base.find_answer(user_message.text, self.personality.name, self.personality.set_personality)
        bot_message = self.personality.reply(raw_response)
        self.history.add_message(bot_message)
        return bot_message

    def start_conversation(self, user: User):
        # definir loop de conversação

        print("Iniciando conversa com o bot. Digite 'sair' para encerrar.")
        print(self.personality.get_greeting().text)

        while True:
            try:
                user_input = input(f"{user.name}: ")
                if user_input.lower() == "sair":
                    self.history.add_message(Message(sender=user.name, text=user_input))
                    self.history.save_session()
                    print(f"{self.personality.name}: Até mais {user.name}!")
                    break
            
                user_message = Message(sender=user.name, text=user_input)
                bot_response = self.process_input(user_message)
                print(f"{self.personality.name}: {bot_response.text}")

            except KeyboardInterrupt:
                print("\nConversa interrompida. Salvando histórico...")
                self.history.save_session()
                break
