import random
from typing import Dict, List, Union

class KnowledgeBase:
    
    def __init__(self, data: Dict[str, Union[str, List[str]]]):
        self.qa = data

    # encontra uma resposta baseada na pergunta
    def find_answer(self, text: str, personality_name: str = 'academico') -> str:
        responses = []
        for intent in self.qa.get('intents', []):
            patterns = intent.get('patterns', [])
            if text in patterns:
                responses = intent.get('responses', [])
                return random.choice(responses.get(personality_name, []))
            
        return "Desculpe, não entendi. Você pode reformular?"
