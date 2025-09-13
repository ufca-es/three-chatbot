from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    from app.routes import bp
    app.register_blueprint(bp)
    return app
