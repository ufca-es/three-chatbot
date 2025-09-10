from app.modules import Chatbot, KnowledgeBase, Personality, History, User, Message
import json
perguntas_json = './app/data/perguntas.json'

# FUNÇÃO RASCUNHO de execução do bot via terminal
def run_chatbot():

    with open(perguntas_json, 'r') as arquivo:
        qa_data = json.load(arquivo)

    knowledge_base = KnowledgeBase(data=qa_data)
    user = User(user_id=1, name="Sebastião")
    history = History()
    
    history.load_last_interactions(num_interactions=6) 
    history.show_last_interactions()
    
    personality = Personality()

    bot = Chatbot(
        personality=personality,
        knowledge_base=knowledge_base,
        history=history
    )

    bot.start_conversation(user)

run_chatbot()