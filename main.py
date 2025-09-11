from app.modules import Chatbot, KnowledgeBase, Personality, History, User
import json

perguntas_json = './app/data/perguntas.json'
aprendizado_json = './app/data/aprendizado.json'

# FUNÇÃO RASCUNHO de execução do bot via terminal
def run_chatbot():
    # carrega perguntas fixas
    with open(perguntas_json, 'r', encoding="utf-8") as arquivo:
        qa_data = json.load(arquivo)

    # carrega aprendizado anterior (se existir)
    try:
        with open(aprendizado_json, 'r', encoding="utf-8") as arquivo:
            nk_data = json.load(arquivo)
    except FileNotFoundError:
        nk_data = {"intents": []}

    knowledge_base = KnowledgeBase(
        data=qa_data,
        new_knowledge_file=nk_data,
        nk_path=aprendizado_json
    )

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


if __name__ == "__main__":
    run_chatbot()
