"""
Model Tests
=============
Tests for SQLAlchemy models.
"""

from app import db
from app.models.user import User
from app.models.conversation import Conversation, Message


def test_create_user(app):
    """Test user creation and password hashing."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("secure123")
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.check_password("secure123")
        assert not user.check_password("wrongpass")


def test_create_conversation(app):
    """Test conversation and message creation."""
    with app.app_context():
        user = User(username="chatuser", email="chat@example.com")
        user.set_password("pass")
        db.session.add(user)
        db.session.commit()

        conv = Conversation(user_id=user.id, title="Test Chat")
        db.session.add(conv)
        db.session.commit()

        msg = Message(conversation_id=conv.id, role="user", content="Hello AI!")
        db.session.add(msg)
        db.session.commit()

        assert len(conv.messages) == 1
        assert conv.messages[0].content == "Hello AI!"
