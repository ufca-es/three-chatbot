from flask import Blueprint, render_template, jsonify, request
from app.modules import Chatbot, KnowledgeBase, Personality, History, User
from app.modules.message import Message
import json, os

bp = Blueprint("routes", __name__)

@bp.route("/")
def landing():
    return render_template("index.html")

@bp.route("/api/status")
def status():
    return jsonify({"status": "ok", "mensagem": "API Flask rodando!"})


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

user = User(user_id=1, name="Sebastião")
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

    return jsonify({
        "user": user_message,
        "bot": bot_msg.text
    })
