"""
Service Tests
==============
Tests for business logic services.
"""

from app.utils.helpers import sanitize_input, truncate_text, safe_json_parse


def test_sanitize_input():
    """Test HTML tag stripping."""
    assert sanitize_input("<script>alert('xss')</script>Hello") == "alert('xss')Hello"
    assert sanitize_input("") == ""
    assert sanitize_input("Normal text") == "Normal text"


def test_truncate_text():
    """Test text truncation."""
    assert truncate_text("Short", 100) == "Short"
    assert len(truncate_text("A " * 100, 50)) <= 53  # 50 + "..."


def test_safe_json_parse():
    """Test safe JSON parsing."""
    assert safe_json_parse('{"key": "value"}') == {"key": "value"}
    assert safe_json_parse("invalid json") == {}
    assert safe_json_parse(None) == {}
