from app.modules import Chatbot, KnowledgeBase, Personality, History, User, Message

# FUNÇÃO RASCUNHO de execução do bot via terminal
def run_chatbot():

    qa_data = {
        "oi": ["Olá! Como vai?", "Oi! Tudo bem por aqui, e com você?", "E aí!"],
        "tudo bem?": "Tudo ótimo! Pronto para ajudar.",
        "qual o seu nome?": "Meu nome é Botinho, mas meus amigos me chamam de Bot.",
        "ajuda": "Eu posso responder perguntas simples. Tente me dizer 'oi' ou perguntar meu nome!",
        "horario": "São 21:02 de Domingo, 7 de Setembro de 2025."
    }

    knowledge_base = KnowledgeBase(data=qa_data)
    user = User(user_id=1, name="Sebastião")
    history = History()
    
    personality = Personality(name="Bot Padrão")

    bot = Chatbot(
        personality=personality,
        knowledge_base=knowledge_base,
        history=history
    )

    print("Iniciando conversa com o bot. Digite 'sair' para encerrar.")
    print(bot.personality.get_greeting().text)

    user_input = input(f"{user.name}: ")
    user_message = Message(sender=user.name, text=user_input)
    bot_response = bot.process_input(user_message)
    print(f"{bot.personality.name}: {bot_response.text}")

run_chatbot()