import random
from typing import Dict, List, Union

class KnowledgeBase:
    
    def __init__(self, data: Dict[str, Union[str, List[str]]]):
        self.qa = data

    # encontra uma resposta baseada na pergunta
    def find_answer(self, pergunta: str) -> str:
        key = pergunta.lower().strip()
        
        if key in self.qa:
            respostas = self.qa[key]

            if isinstance(respostas, list):
                return random.choice(respostas)
            return respostas
            
        return "Desculpe, não entendi. Você pode reformular?"

    # adiciona novo par pergunta-resposta
    def new_knowledge(self, pergunta: str, resposta: str):
        key = pergunta.lower().strip()
        self.qa[key] = resposta
        print(f"(Aprendizado adicionado: '{key}' -> '{resposta}')")
