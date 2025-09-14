from .user import User
from .knowledgebase import KnowledgeBase
from .personality import Personality
from .history import History
from .message import Message
from collections import Counter
import json
import unicodedata
import re

class Chatbot:
    def __init__(self, personality: Personality, knowledge_base: KnowledgeBase, history: History):
        self.personality = personality
        self.knowledge_base = knowledge_base
        self.history = history
        self.personality_usage = Counter()
        self.personality_usage[self.personality.name] += 1

    def set_personality(self, new_personality_name: str):
        if self.personality.name != new_personality_name:
            self.personality.set_personality(new_personality_name)
            self.personality_usage[new_personality_name] += 1
    
    def process_input(self, user_message: Message) -> Message:
        """
        Recebe uma mensagem do usuário, consulta a base de conhecimento
        e retorna a resposta do bot como Message.
        """
        self.history.add_message(user_message)

        raw_response = self.knowledge_base.find_answer(
            self.normalize_text(user_message.text),
            self.personality.name,
            self.set_personality
        )

        if raw_response is None:
            raw_response = "Ainda não sei responder isso. Quer me ensinar?"
            bot_message = self.personality.reply(raw_response)
            self.history.add_message(bot_message)

        else:
            bot_message = self.personality.reply(raw_response)
            self.history.add_message(bot_message)

        return bot_message

    def save_stats_to_file(self, stats_filename="stats.json"):
        last_user_message = self.history.get_last_user_message()

        try:
            with open(stats_filename, 'r', encoding='utf-8') as f:
                overall_stats = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            overall_stats = {
                "total_interactions": 0,
                "question_counts": {},
                "personality_counts": {}
            }

        ignored_tags = ["saudacao", "agradecimento", "despedida", "riso", "personalidade_academico", "personalidade_gamificado", "personalidade_acessivel"]

        session_interaction_count = 0
        tag = self.knowledge_base.find_tag_for_text(last_user_message)
        if tag and tag not in ignored_tags:
            session_interaction_count += 1
            question = last_user_message.lower()
            overall_stats["question_counts"][question] = overall_stats["question_counts"].get(question, 0) + 1
        
        overall_stats["total_interactions"] += 1
        for personality, count in self.personality_usage.items():
            overall_stats["personality_counts"][personality] = overall_stats["personality_counts"].get(personality, 0) + count

        with open(stats_filename, 'w', encoding='utf-8') as f:
            json.dump(overall_stats, f, ensure_ascii=False, indent=4)
        
        print("(Estatísticas globais salvas com sucesso!)")


    def normalize_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""

        text_without_accents = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

        lower_case_text = text_without_accents.lower()
        final_text = re.sub(r'[^a-z\s]', '', lower_case_text)

        return final_text
