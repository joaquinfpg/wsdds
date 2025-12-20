from flask import Flask
from config import Config
from database import db
from features.vpsearch.routes import vpsearch_bp
from features.chat import chat_bp


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    # Set a secret key for session support
    app.secret_key = getattr(Config, 'SECRET_KEY', None) or 'change-this-secret-key'

    db.init_app(app)
    app.register_blueprint(vpsearch_bp)
    app.register_blueprint(chat_bp, url_prefix='/chat')


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
