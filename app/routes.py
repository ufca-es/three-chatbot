from flask import Blueprint, render_template, jsonify, request
from app.modules import Chatbot, KnowledgeBase, Personality, History, User
from app.modules.message import Message
import json, os

bp = Blueprint("routes", __name__)

@bp.route("/")
def landing():
    return render_template("index.html")

perguntas_json = './app/data/perguntas.json'
aprendizado_json = './app/data/aprendizado.json'

with open(perguntas_json, 'r', encoding="utf-8") as arquivo:
    qa_data = json.load(arquivo)

if os.path.exists(aprendizado_json):
    with open(aprendizado_json, 'r', encoding="utf-8") as arquivo:
        nk_data = json.load(arquivo)
else:
    nk_data = {"intents": []}

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


@bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Mensagem vazia."}), 400

    user_msg = Message(sender=user.name, text=user_message)
    bot_msg = bot.process_input(user_msg, user)

    history.save_session()
    bot.save_stats_to_file()

    return jsonify({
        "user": user_message,
        "bot": bot_msg.text
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