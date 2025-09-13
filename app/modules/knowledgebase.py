import json
import random
from typing import Dict, List, Union, Callable
from .user import User
from .history import History
from .message import Message


class KnowledgeBase:
    def __init__(self, data, new_knowledge_file, nk_path):
        self.qa = data
        self.new_knowledge_file = new_knowledge_file
        self.nk_path = nk_path

    def find_answer(
        self,
        text: str,
        personality_name: str = 'academico',
        set_personality: Callable[[str], None] = None,
        user: User = None
    ) -> str:

        for action in self.qa.get('actions', []):
            patterns = action.get('patterns', [])
            if text in patterns:
                action_name = action["do"]
                if set_personality:
                    set_personality(action_name)
                return random.choice(action.get('responses', []))

        for intent in self.qa.get('intents', []):
            patterns = intent.get('patterns', [])
            if text in patterns:
                responses = intent.get('responses', {})
                if personality_name in responses and responses[personality_name]:
                    return random.choice(responses[personality_name])
                elif "default" in responses and responses["default"]:
                    return random.choice(responses["default"])
                else:
                    return "Erro ao processar sua pergunta. Tente novamente."

        for intent in self.new_knowledge_file.get('intents', []):
            patterns = intent.get('patterns', [])
            if text in patterns:
                responses = intent.get('responses', {})
                if personality_name in responses and responses[personality_name]:
                    return random.choice(responses[personality_name])
                elif "default" in responses and responses["default"]:
                    return random.choice(responses["default"])
                else:
                    return "Erro ao processar sua pergunta. Tente novamente."

        return None


    def new_knowledge(self, text: str, resposta: str) -> bool:
        """
        Adiciona novo conhecimento ao arquivo de aprendizado.
        """
        if not resposta:
            return False

        new_data = {
            "tag": "aprendizado",
            "patterns": [text],
            "responses": {
                "default": [resposta]
            }
        }

        if "intents" not in self.new_knowledge_file:
            self.new_knowledge_file["intents"] = []

        self.new_knowledge_file["intents"].append(new_data)
        
        try:
            with open(self.nk_path, "w", encoding="utf-8") as f:
                json.dump(self.new_knowledge_file, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar aprendizado: {e}")
            return False
        
    def find_tag_for_text(self, text: str) -> str:
        # Encontra e retorna a tag para um determinado texto, se existir.
        text_lower = text.lower()
        for intent in self.qa.get('intents', []):
            for pattern in intent.get('patterns', []):
                if pattern.lower() in text_lower:
                    return intent['tag']
        for intent in self.new_knowledge_file.get('intents', []):
            for pattern in intent.get('patterns', []):
                if pattern.lower() in text_lower:
                    return intent['tag']
        return None
