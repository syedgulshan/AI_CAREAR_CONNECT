"""
Speech Routes
==============
Endpoints for speech-to-text and text-to-speech conversion.
"""

import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from app.services.stt_service import stt_service
from app.services.tts_service import tts_service

speech_bp = Blueprint("speech", __name__)


@speech_bp.route("/stt", methods=["POST"])
@login_required
def speech_to_text():
    """
    Convert uploaded audio file to text.
    Expects a multipart form with an 'audio' file field.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save temp file
    temp_dir = os.path.join(current_app.static_folder, "audio")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"temp_{uuid.uuid4().hex[:8]}.wav")
    audio_file.save(temp_path)

    # Convert
    result = stt_service.from_audio_file(temp_path)

    # Cleanup temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if result["success"]:
        return jsonify({"text": result["text"]})
    else:
        return jsonify({"error": result["error"]}), 422


@speech_bp.route("/tts", methods=["POST"])
@login_required
def text_to_speech():
    """
    Convert text to speech audio file.
    Expects JSON body with a 'text' field.
    Returns the URL path to the generated audio file.
    """
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = tts_service.synthesize(text)

    if result["success"]:
        return jsonify({"audio_url": result["audio_path"]})
    else:
        return jsonify({"error": result["error"]}), 500
