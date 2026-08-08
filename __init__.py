"""
AI Career Connect - Application Factory
=========================================
Uses the Flask "Application Factory" pattern so the app can be
created with different configurations (dev / test / prod).
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# ── Shared extension instances (initialized once, bound in create_app) ──
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name="development"):
    """Create and configure the Flask application."""

    # Load .env variables before anything reads os.environ
    load_dotenv()

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="static",
        template_folder="templates",
    )

    # ── Load configuration ──
    from app.config import config_dict
    app.config.from_object(config_dict.get(config_name, config_dict["development"]))

    # ── Initialize extensions ──
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # ── Register Blueprints (route groups) ──
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.ai_chat import ai_chat_bp
    from app.routes.speech import speech_bp
    from app.routes.career import career_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ai_chat_bp, url_prefix="/api/chat")
    app.register_blueprint(speech_bp, url_prefix="/api/speech")
    app.register_blueprint(career_bp, url_prefix="/api/career")

    # ── Create database tables ──
    with app.app_context():
        from app.models import user, career, conversation  # noqa: F401
        db.create_all()

    return app
