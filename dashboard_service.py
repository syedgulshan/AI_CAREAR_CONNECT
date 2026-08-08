"""
Dashboard Service
==================
Aggregates data for the dynamic dashboard:
conversation stats, career progress, and activity metrics.
"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from app import db
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.models.career import CareerProfile, Roadmap


class DashboardService:
    """Computes dashboard analytics and metrics."""

    @staticmethod
    def get_user_stats(user_id: int) -> dict:
        """
        Aggregate key metrics for a user's dashboard.

        Returns:
            dict with keys: total_conversations, total_messages,
            total_profiles, total_roadmaps, recent_activity.
        """
        total_conversations = Conversation.query.filter_by(user_id=user_id).count()
        total_messages = (
            db.session.query(func.count(Message.id))
            .join(Conversation)
            .filter(Conversation.user_id == user_id)
            .scalar()
        )
        total_profiles = CareerProfile.query.filter_by(user_id=user_id).count()
        total_roadmaps = (
            db.session.query(func.count(Roadmap.id))
            .join(CareerProfile)
            .filter(CareerProfile.user_id == user_id)
            .scalar()
        )

        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_profiles": total_profiles,
            "total_roadmaps": total_roadmaps,
        }

    @staticmethod
    def get_recent_conversations(user_id: int, limit: int = 5) -> list:
        """Return the most recent conversations for a user."""
        return (
            Conversation.query.filter_by(user_id=user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_activity_timeline(user_id: int, days: int = 7) -> list:
        """
        Get daily message counts for the past N days.
        Used to render activity charts on the dashboard.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        results = (
            db.session.query(
                func.date(Message.created_at).label("date"),
                func.count(Message.id).label("count"),
            )
            .join(Conversation)
            .filter(Conversation.user_id == user_id, Message.created_at >= cutoff)
            .group_by(func.date(Message.created_at))
            .order_by(func.date(Message.created_at))
            .all()
        )
        return [{"date": str(r.date), "count": r.count} for r in results]


# ── Singleton instance ──
dashboard_service = DashboardService()
