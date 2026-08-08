"""
Career Routes
==============
Endpoints for career profile management, resume analysis,
interview question generation, and roadmap creation.
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.services.career_service import career_service
from app.services.mistral_service import mistral_service

career_bp = Blueprint("career", __name__)


@career_bp.route("/profile", methods=["GET"])
@login_required
def career_profile_page():
    """Render the career profile page."""
    profiles = career_service.get_user_profiles(current_user.id)
    return render_template("career/profile.html", profiles=profiles)


@career_bp.route("/profile", methods=["POST"])
@login_required
def create_profile():
    """Create a new career profile."""
    data = request.json
    profile = career_service.create_profile(current_user.id, data)
    return jsonify({
        "id": profile.id,
        "current_role": profile.current_role,
        "desired_role": profile.desired_role,
    }), 201


@career_bp.route("/roadmap/<int:profile_id>", methods=["POST"])
@login_required
def generate_roadmap(profile_id):
    """Generate an AI career roadmap for a profile."""
    roadmap = career_service.generate_roadmap(profile_id)
    return jsonify({
        "id": roadmap.id,
        "title": roadmap.title,
        "content": roadmap.content,
    })


@career_bp.route("/resume", methods=["GET"])
@login_required
def resume_page():
    """Render the Resume Analyzer page."""
    return render_template("career/resume.html")


@career_bp.route("/interview", methods=["GET"])
@login_required
def interview_page():
    """Render the Interview Question Analyzer page."""
    return render_template("career/interview.html")


@career_bp.route("/resume/analyze", methods=["POST"])
@login_required
def analyze_resume():
    """Analyze a resume and return AI feedback."""
    data = request.json
    resume_text = data.get("resume_text", "")
    if not resume_text.strip():
        return jsonify({"error": "No resume text provided"}), 400

    analysis = mistral_service.analyze_resume(resume_text)
    return jsonify({"analysis": analysis})


@career_bp.route("/interview/questions", methods=["POST"])
@login_required
def get_interview_questions():
    """Generate interview questions for a role."""
    data = request.json
    role = data.get("role", "Software Engineer")
    skills = data.get("skills", "")

    questions = mistral_service.generate_interview_questions(role, skills)
    return jsonify({"questions": questions})
