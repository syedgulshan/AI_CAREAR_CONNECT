"""
AI Career Connect - Configuration
===================================
Centralizes all app settings. Each environment (dev/test/prod)
gets its own class so you never mix debug flags with production secrets.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Shared settings across all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mistral AI
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL = "mistral-large-latest"

    # Speech
    SPEECH_LANGUAGE = os.getenv("SPEECH_LANGUAGE", "en-US")
    TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")

    # Upload limits (16 MB max for audio files)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(BaseConfig):
    """Local development — debug ON, SQLite in instance/."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'ai_career_connect.db')}"
    )


class TestingConfig(BaseConfig):
    """Automated tests — in-memory SQLite, WTF-CSRF off."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production — debug OFF, reads DATABASE_URL from env."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


# ── Quick lookup dict used by create_app() ──
config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
