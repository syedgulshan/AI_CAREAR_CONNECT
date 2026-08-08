"""
Mistral AI Service
===================
Handles all communication with the Mistral API.
Provides methods for career advice, resume analysis,
interview prep, and roadmap generation.
"""

import os
import json
from mistralai import Mistral


class MistralService:
    """Wrapper around the Mistral AI client."""

    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY", "")
        self.client = Mistral(api_key=api_key)
        self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    # ── Core chat completion ──
    def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        """
        Send a list of messages to Mistral and return the assistant reply.

        Args:
            messages: List of dicts with 'role' and 'content' keys.
            temperature: Creativity control (0.0 = deterministic, 1.0 = creative).

        Returns:
            The assistant's text response.
        """
        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content

    # ── Domain-specific helpers ──
    def career_advice(self, user_message: str, context: str = "") -> str:
        """Get career guidance from the AI."""
        system_prompt = (
            "You are an expert AI career counselor. Provide specific, actionable "
            "career advice. Consider the user's background when provided. "
            "Be encouraging but realistic."
        )
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        if context:
            messages.append({"role": "system", "content": f"User context: {context}"})
        messages.append({"role": "user", "content": user_message})
        return self.chat(messages)

    def analyze_resume(self, resume_text: str) -> str:
        """Analyze a resume and provide improvement suggestions."""
        system_prompt = (
            "You are a professional resume reviewer. Analyze the following resume "
            "and provide: 1) Strengths, 2) Weaknesses, 3) Specific improvement "
            "suggestions, 4) ATS optimization tips. Be constructive and detailed."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please analyze this resume:\n\n{resume_text}"},
        ]
        return self.chat(messages, temperature=0.5)

    def generate_interview_questions(self, role: str, skills: str = "") -> str:
        """Generate interview questions for a specific role."""
        system_prompt = (
            "You are an expert technical interviewer. Generate a set of interview "
            "questions including: behavioral, technical, and situational questions. "
            "Provide expected answer guidelines for each question."
        )
        prompt = f"Generate interview questions for a {role} position."
        if skills:
            prompt += f" The candidate has these skills: {skills}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        return self.chat(messages, temperature=0.6)

    def generate_roadmap(self, current_role: str, desired_role: str, skills: str = "") -> str:
        """Generate a career transition roadmap."""
        system_prompt = (
            "You are a career strategist. Create a detailed, step-by-step career "
            "roadmap with timelines, required skills, resources, and milestones. "
            "Format the response as structured JSON with keys: title, summary, "
            "milestones (array of {phase, duration, goals, resources})."
        )
        prompt = (
            f"Create a career roadmap from '{current_role}' to '{desired_role}'."
        )
        if skills:
            prompt += f" Current skills: {skills}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        return self.chat(messages, temperature=0.5)


# ── Singleton instance ──
mistral_service = MistralService()
