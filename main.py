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
    
    personality = Personality()

    bot = Chatbot(
        personality=personality,
        knowledge_base=knowledge_base,
        history=history
    )

    print("Iniciando conversa com o bot. Digite 'sair' para encerrar.\n")

    user_input = input(f"{user.name}: ")
    user_message = Message(sender=user.name, text=user_input)
    bot_response = bot.process_input(user_message)
    print(f"{bot.personality.name}: {bot_response.text}")

run_chatbot()