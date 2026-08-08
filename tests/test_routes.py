"""
Route Tests
=============
Tests for Flask route endpoints.
"""


def test_login_page(client):
    """Test that login page loads successfully."""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page(client):
    """Test that register page loads successfully."""
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b"Create Account" in response.data


def test_unauthenticated_redirect(client):
    """Test that dashboard redirects unauthenticated users."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
