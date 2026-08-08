"""
Speech-to-Text Service
=======================
Converts audio input (microphone or uploaded file) into text
using the SpeechRecognition library with Google's free API.
"""

import os
import speech_recognition as sr


class STTService:
    """Speech-to-Text conversion service."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = os.getenv("SPEECH_LANGUAGE", "en-US")

    def from_microphone(self) -> dict:
        """
        Capture audio from the default microphone and convert to text.

        Returns:
            dict: {"success": bool, "text": str, "error": str | None}
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
            text = self.recognizer.recognize_google(audio, language=self.language)
            return {"success": True, "text": text, "error": None}
        except sr.UnknownValueError:
            return {"success": False, "text": "", "error": "Could not understand the audio."}
        except sr.RequestError as e:
            return {"success": False, "text": "", "error": f"Speech service error: {e}"}
        except sr.WaitTimeoutError:
            return {"success": False, "text": "", "error": "No speech detected within timeout."}

    def from_audio_file(self, file_path: str) -> dict:
        """
        Convert an audio file (WAV/FLAC/AIFF) to text.

        Args:
            file_path: Absolute path to the audio file.

        Returns:
            dict: {"success": bool, "text": str, "error": str | None}
        """
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio, language=self.language)
            return {"success": True, "text": text, "error": None}
        except sr.UnknownValueError:
            return {"success": False, "text": "", "error": "Could not understand the audio."}
        except sr.RequestError as e:
            return {"success": False, "text": "", "error": f"Speech service error: {e}"}
        except FileNotFoundError:
            return {"success": False, "text": "", "error": "Audio file not found."}


# ── Singleton instance ──
stt_service = STTService()
