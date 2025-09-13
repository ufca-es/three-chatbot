from flask import Blueprint, render_template, jsonify, request, session
from app.modules import Chatbot, KnowledgeBase, Personality, History, User
from app.modules.message import Message
import json, os

# --- IMPORTANTE: A SECRET_KEY DEVE ESTAR CONFIGURADA NO ARQUIVO PRINCIPAL DA APLICAÇÃO ---
bp = Blueprint("routes", __name__)

# --- INICIALIZAÇÃO DO BOT (Como no seu código original) ---
perguntas_json = './app/data/perguntas.json'
aprendizado_json = './app/data/aprendizado.json'

with open(perguntas_json, 'r', encoding="utf-8") as arquivo:
    qa_data = json.load(arquivo)

if os.path.exists(aprendizado_json):
    with open(aprendizado_json, 'r', encoding="utf-8") as arquivo:
        nk_data = json.load(arquivo)
else:
    nk_data = {"intents": []}
    with open(aprendizado_json, 'w', encoding="utf-8") as arquivo:
        json.dump(nk_data, arquivo, ensure_ascii=False, indent=4)

knowledge_base = KnowledgeBase(
    data=qa_data,
    new_knowledge_file=nk_data,
    nk_path=aprendizado_json
)

user = User(user_id=1, name="user")
history = History()
personality = Personality()

bot = Chatbot(
    personality=personality,
    knowledge_base=knowledge_base,
    history=history
)

# Mensagem que ativa o modo de aprendizado
LEARNING_TRIGGER_PHRASE = "Ainda não sei responder isso. Quer me ensinar?"

@bp.route("/")
def landing():
    session.pop('learning_mode', None)
    session.pop('original_question', None)
    return render_template("index.html")

@bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Mensagem vazia."}), 400

    # --- LÓGICA DE APRENDIZADO ---
    # Passo 2: Se o bot está em modo de aprendizado, a mensagem atual é a resposta.
    if session.get('learning_mode'):
        new_answer = user_message
        original_question = session.get('original_question')
        
        # CHAMA A FUNÇÃO CORRETA: new_knowledge
        knowledge_base.new_knowledge(
            text=original_question,
            resposta=new_answer
        )

        # Limpa a sessão para sair do modo de aprendizado
        session.pop('learning_mode', None)
        session.pop('original_question', None)
        
        bot_response_text = "Entendi! Aprendi algo novo. Obrigado! 👍"
        return jsonify({"user": user_message, "bot": bot_response_text})

    # --- FLUXO NORMAL DA CONVERSA ---
    user_msg = Message(sender=user.name, text=user_message)
    bot_msg = bot.process_input(user_msg, user)
    bot_response_text = bot_msg.text

    # Passo 1: Se o bot não soube responder, ele ativa o modo de aprendizado.
    if bot_response_text == LEARNING_TRIGGER_PHRASE:
        session['learning_mode'] = True
        session['original_question'] = user_message
        bot_response_text = "Hmm, essa eu não sei. Qual seria a resposta correta?"

    history.save_session()
    bot.save_stats_to_file()

    return jsonify({
        "user": user_message,
        "bot": bot_response_text
    })

@bp.route("/api/stats")
def stats():
    try:
        with open("stats.json", "r", encoding="utf-8") as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stats = {
            "total_interactions": 0,
            "question_counts": {},
            "personality_counts": {}
        }
    return jsonify(stats)

@bp.route("/api/report")
def report():
    try:
        with open("relatorio.txt", "r", encoding="utf-8") as f:
            relatorio = f.read()
    except FileNotFoundError:
        relatorio = "Relatório ainda não gerado."
    return jsonify({"relatorio": relatorio})

