"""
Career Service
===============
Business logic for career profile management,
roadmap generation, and resume analysis orchestration.
"""

from app import db
from app.models.career import CareerProfile, Roadmap
from app.services.mistral_service import mistral_service


class CareerService:
    """Orchestrates career-related operations."""

    @staticmethod
    def create_profile(user_id: int, data: dict) -> CareerProfile:
        """Create a new career profile for a user."""
        profile = CareerProfile(
            user_id=user_id,
            current_role=data.get("current_role", ""),
            desired_role=data.get("desired_role", ""),
            experience_years=data.get("experience_years", 0),
            skills=data.get("skills", ""),
            education=data.get("education", ""),
            interests=data.get("interests", ""),
        )
        db.session.add(profile)
        db.session.commit()
        return profile

    @staticmethod
    def generate_roadmap(profile_id: int) -> Roadmap:
        """Generate an AI-powered career roadmap for a profile."""
        profile = CareerProfile.query.get_or_404(profile_id)

        # Call Mistral to generate the roadmap
        content = mistral_service.generate_roadmap(
            current_role=profile.current_role or "Student",
            desired_role=profile.desired_role or "Software Engineer",
            skills=profile.skills or "",
        )

        roadmap = Roadmap(
            profile_id=profile.id,
            title=f"Roadmap: {profile.current_role} → {profile.desired_role}",
            content=content,
        )
        db.session.add(roadmap)
        db.session.commit()
        return roadmap

    @staticmethod
    def get_user_profiles(user_id: int) -> list:
        """Fetch all career profiles for a user."""
        return CareerProfile.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_profile_roadmaps(profile_id: int) -> list:
        """Fetch all roadmaps for a career profile."""
        return Roadmap.query.filter_by(profile_id=profile_id).all()


# ── Singleton instance ──
career_service = CareerService()
