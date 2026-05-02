from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user_optional
from app.auth.models import UserResponse
from app.main import app
from app.round.transport.get_db_session import get_db_session


def test_start_route_allows_guest_without_bearer_token():
    """Practice mode is open to guests; no token should still return a round."""
    app.dependency_overrides[get_current_user_optional] = lambda: None
    app.dependency_overrides[get_db_session] = lambda: MagicMock()

    try:
        client = TestClient(app)
        response = client.post("/round/start")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert "round_id" in payload["data"]
    assert "target_image_url" in payload["data"]


def test_start_route_returns_payload_with_authenticated_user():
    app.dependency_overrides[get_current_user_optional] = lambda: UserResponse(
        id="u1",
        email="u1@example.com",
        name="User One",
    )
    app.dependency_overrides[get_db_session] = lambda: MagicMock()

    try:
        client = TestClient(app)
        response = client.post(
            "/round/start", headers={"Authorization": "Bearer test-token"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert "round_id" in payload["data"]
    assert "target_image_url" in payload["data"]
