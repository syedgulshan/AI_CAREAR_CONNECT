"""
AI Chat Routes
================
Handles conversations with the Mistral AI assistant.
Supports creating conversations, sending messages,
and retrieving chat history.
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models.conversation import Conversation, Message
from app.services.mistral_service import mistral_service

ai_chat_bp = Blueprint("ai_chat", __name__)


@ai_chat_bp.route("/", methods=["GET"])
@login_required
def chat_page():
    """Render the chat interface."""
    conversations = (
        Conversation.query.filter_by(user_id=current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    return render_template("chat/index.html", conversations=conversations)


@ai_chat_bp.route("/conversations", methods=["POST"])
@login_required
def create_conversation():
    """Create a new conversation."""
    title = request.json.get("title", "New Conversation")
    conv = Conversation(user_id=current_user.id, title=title)
    db.session.add(conv)
    db.session.commit()
    return jsonify({"id": conv.id, "title": conv.title}), 201


@ai_chat_bp.route("/conversations/<int:conv_id>/messages", methods=["GET"])
@login_required
def get_messages(conv_id):
    """Get all messages in a conversation."""
    conv = Conversation.query.get_or_404(conv_id)
    messages = [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "is_voice": m.is_voice,
            "created_at": m.created_at.isoformat(),
        }
        for m in conv.messages
    ]
    return jsonify(messages)


@ai_chat_bp.route("/conversations/<int:conv_id>/send", methods=["POST"])
@login_required
def send_message(conv_id):
    """Send a message and get an AI response."""
    conv = Conversation.query.get_or_404(conv_id)
    data = request.json
    user_text = data.get("message", "").strip()
    is_voice = data.get("is_voice", False)

    if not user_text:
        return jsonify({"error": "Empty message"}), 400

    # Save user message
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=user_text,
        is_voice=is_voice,
    )
    db.session.add(user_msg)

    # Build message history for context
    history = [{"role": m.role, "content": m.content} for m in conv.messages]
    history.append({"role": "user", "content": user_text})

    # Get AI response
    ai_response = mistral_service.career_advice(user_text)

    # Save AI message
    ai_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=ai_response,
    )
    db.session.add(ai_msg)
    db.session.commit()

    return jsonify({
        "user_message": {"id": user_msg.id, "content": user_text},
        "ai_response": {"id": ai_msg.id, "content": ai_response},
    })


@ai_chat_bp.route("/conversations/<int:conv_id>", methods=["DELETE"])
@login_required
def delete_conversation(conv_id):
    """Delete a conversation and all its messages."""
    conv = Conversation.query.get_or_404(conv_id)
    Message.query.filter_by(conversation_id=conv.id).delete()
    db.session.delete(conv)
    db.session.commit()
    return jsonify({"message": "Conversation deleted"}), 200
