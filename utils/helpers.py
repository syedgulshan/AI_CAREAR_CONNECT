"""
Helper Utilities
=================
General-purpose helper functions used throughout the application.
"""

import re
import json
from datetime import datetime, timezone


def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r"<[^>]+>", "", text)
    return clean.strip()


def format_timestamp(dt: datetime) -> str:
    """Format a datetime object into a human-readable string."""
    if not dt:
        return ""
    return dt.strftime("%b %d, %Y at %I:%M %p")


def safe_json_parse(text: str, default=None):
    """Safely parse a JSON string, returning default on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default if default is not None else {}


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length with ellipsis."""
    if not text or len(text) <= max_length:
        return text or ""
    return text[:max_length].rsplit(" ", 1)[0] + "..."
