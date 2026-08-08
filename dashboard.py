"""
Dashboard Routes
=================
Serves the dynamic dashboard with user stats, recent activity,
career progress, and quick actions.
"""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.services.dashboard_service import dashboard_service

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    """Main dashboard page."""
    stats = dashboard_service.get_user_stats(current_user.id)
    recent = dashboard_service.get_recent_conversations(current_user.id)
    return render_template(
        "dashboard/index.html",
        stats=stats,
        recent_conversations=recent,
    )


@dashboard_bp.route("/api/dashboard/stats")
@login_required
def api_stats():
    """JSON endpoint for dashboard stats (used by JS charts)."""
    stats = dashboard_service.get_user_stats(current_user.id)
    return jsonify(stats)


@dashboard_bp.route("/api/dashboard/activity")
@login_required
def api_activity():
    """JSON endpoint for activity timeline chart data."""
    days = int(request_args_get("days", 7))
    timeline = dashboard_service.get_activity_timeline(current_user.id, days=days)
    return jsonify(timeline)


def request_args_get(key, default=None):
    """Helper to safely get request args."""
    from flask import request
    return request.args.get(key, default)
