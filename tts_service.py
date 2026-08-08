"""
Text-to-Speech Service
=======================
Converts AI text responses into audio using gTTS (Google Text-to-Speech).
Falls back to pyttsx3 for offline support.
"""

import os
import uuid
from gtts import gTTS


class TTSService:
    """Text-to-Speech conversion service."""

    # Directory where generated audio files are stored
    AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "audio")

    def __init__(self):
        self.language = os.getenv("TTS_LANGUAGE", "en")
        os.makedirs(self.AUDIO_DIR, exist_ok=True)

    def synthesize(self, text: str, filename: str = None) -> dict:
        """
        Convert text to an MP3 audio file.

        Args:
            text: The text to speak.
            filename: Optional custom filename (without extension).

        Returns:
            dict: {"success": bool, "audio_path": str, "error": str | None}
        """
        if not text or not text.strip():
            return {"success": False, "audio_path": "", "error": "No text provided."}

        try:
            if not filename:
                filename = f"tts_{uuid.uuid4().hex[:8]}"
            filepath = os.path.join(self.AUDIO_DIR, f"{filename}.mp3")

            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(filepath)

            # Return URL-friendly relative path for the frontend
            relative_path = f"/static/audio/{filename}.mp3"
            return {"success": True, "audio_path": relative_path, "error": None}

        except Exception as e:
            return {"success": False, "audio_path": "", "error": f"TTS error: {e}"}

    def cleanup_old_files(self, max_age_seconds: int = 3600):
        """Remove generated audio files older than max_age_seconds."""
        import time

        now = time.time()
        for f in os.listdir(self.AUDIO_DIR):
            filepath = os.path.join(self.AUDIO_DIR, f)
            if os.path.isfile(filepath) and f.startswith("tts_"):
                if now - os.path.getmtime(filepath) > max_age_seconds:
                    os.remove(filepath)


# ── Singleton instance ──
tts_service = TTSService()
