"""
Custom Decorators
==================
Reusable decorators for route protection,
rate limiting, and request validation.
"""

from functools import wraps
from flask import jsonify, request
from flask_login import current_user


def json_required(f):
    """Ensure the request body is valid JSON."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Restrict access to admin users (extend User model with is_admin)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "Authentication required"}), 401
        # Extend: check current_user.is_admin if you add that field
        return f(*args, **kwargs)
    return decorated
