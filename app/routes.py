from flask import Blueprint, render_template, jsonify

bp = Blueprint("routes", __name__)

@bp.route("/")
def landing():
    return render_template("index.html")

@bp.route("/help")
def help_page():
    return render_template("help.html")

@bp.route("/api/status")
def status():
    return jsonify({"status": "ok", "mensagem": "API Flask rodando!"})
