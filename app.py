from flask import Flask
from flask_login import LoginManager
from config import Config
from database import db, ensure_user_role_column
from features.vpsearch.routes import vpsearch_bp
from features.vpsearch.api import agpro_api_bp
from features.chat import chat_bp
from features.auth.routes import auth_bp
from features.claims.routes import claims_bp
from features.users.models import User
import features.locations.models  # ensure location/dealership tables exist


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    return User.query.get(int(user_id))


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    # Set a secret key for session support
    app.secret_key = getattr(Config, 'SECRET_KEY', None) or 'change-this-secret-key'

    db.init_app(app)
    with app.app_context():
        ensure_user_role_column(db.engine)
    login_manager.init_app(app)
    app.register_blueprint(vpsearch_bp)
    app.register_blueprint(agpro_api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(claims_bp)
    app.register_blueprint(chat_bp, url_prefix='/chat')


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
