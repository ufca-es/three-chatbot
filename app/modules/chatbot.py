from .user import User
from .knowledgebase import KnowledgeBase
from .personality import Personality
from .history import History
from .message import Message
from collections import Counter
import json

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
    
    def process_input(self, user_message: Message, user: User) -> Message:
        self.history.add_message(user_message)

        raw_response = self.knowledge_base.find_answer(
            user_message.text,
            self.personality.name,
            self.set_personality,
            user
        )

        if raw_response is None:
            # pede ao usuário ensinar
            print(f"{self.personality.name}: Não sei responder isso ainda. O que devo responder quando alguém disser '{user_message.text}'?")
            nova_resposta = input(f"{user.name}: ")

            if self.knowledge_base.new_knowledge(user_message.text, nova_resposta):
                raw_response = "Entendi. Obrigado por compartilhar essas informações comigo!"
            else:
                raw_response = "Não consegui aprender essa informação."

        bot_message = self.personality.reply(raw_response)
        self.history.add_message(bot_message)
        return bot_message

    def show_session_summary(self):
        session_stats = self.history.get_session_stats()

        print("\n--- Resumo da Sessão ---")
        print(f"Total de interações do usuário: {session_stats['user_interactions']}")
        
        print("Uso de personalidades:")
        if not self.personality_usage:
            print("Nenhuma personalidade foi usada.")
        else:
            for personality, count in self.personality_usage.items():
                print(f"  - {personality.capitalize()}: {count} vez(es)")
        print("--------------------------\n")

    def save_stats_to_file(self, stats_filename="stats.json"):
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
        
        user_messages = [
            msg for msg in self.history.session_messages if msg.sender.lower() not in ['academico', 'gamificado', 'acessivel']
        ]

        session_interaction_count = 0
        for msg in user_messages:
            tag = self.knowledge_base.find_tag_for_text(msg.text)
            if tag and tag not in ignored_tags:
                session_interaction_count += 1
                question = msg.text.lower()
                overall_stats["question_counts"][question] = overall_stats["question_counts"].get(question, 0) + 1
        
        overall_stats["total_interactions"] += session_interaction_count
        for personality, count in self.personality_usage.items():
            overall_stats["personality_counts"][personality] = overall_stats["personality_counts"].get(personality, 0) + count

        with open(stats_filename, 'w', encoding='utf-8') as f:
            json.dump(overall_stats, f, ensure_ascii=False, indent=4)
        
        print("(Estatísticas globais salvas com sucesso!)")

    def start_conversation(self, user: User):
        print("Iniciando conversa com o bot. Digite 'sair' para encerrar.")
        print(self.personality.get_greeting().text)

        while True:
            try:
                user_input = input(f"{user.name}: ")
                if user_input.lower() == "sair":
                    print(f"{self.personality.name}: Até mais {user.name}!")
                    self.history.add_message(Message(sender=user.name, text=user_input))
                    self.history.save_session()
                    self.save_stats_to_file()
                    self.show_session_summary()
                    break

                user_message = Message(sender=user.name, text=user_input)
                bot_response = self.process_input(user_message, user)
                print(f"{self.personality.name}: {bot_response.text}")

            except KeyboardInterrupt:
                print("\nConversa interrompida. Salvando histórico...")
                self.history.save_session()
                self.save_stats_to_file()
                self.show_session_summary()
                break
