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
        raw_response = self.knowledge_base.find_answer(user_message.text)
        bot_message = self.personality.reply(raw_response)
        self.history.add_message(bot_message)
        return bot_message

    def start_conversation(self, user: User):
        # definir loop de conversação
        return
