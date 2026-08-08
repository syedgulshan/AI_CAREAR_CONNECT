"""
Conversation Models
====================
Persists chat history between a user and the Mistral AI assistant.
"""

from datetime import datetime, timezone
from app import db


class Conversation(db.Model):
    """A chat session between a user and the AI assistant."""

    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), default="New Conversation")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ──
    messages = db.relationship(
        "Message", backref="conversation", lazy=True, order_by="Message.created_at"
    )

    def __repr__(self):
        return f"<Conversation #{self.id} '{self.title}'>"


class Message(db.Model):
    """A single message within a Conversation."""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer, db.ForeignKey("conversations.id"), nullable=False
    )
    role = db.Column(db.String(20), nullable=False)         # 'user' | 'assistant'
    content = db.Column(db.Text, nullable=False)
    is_voice = db.Column(db.Boolean, default=False)         # True if sent via speech
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Message {self.role} in Conv#{self.conversation_id}>"
