import importlib
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.challenge.transport.get_db_session import get_db_session
from app.main import app

view_module = importlib.import_module("app.challenge.service.get_current_challenge_view")


def test_current_route_requires_bearer_token():
    client = TestClient(app)
    response = client.get("/challenge/current")
    assert response.status_code == 401


def test_current_route_returns_payload_with_authenticated_user():
    challenge = MagicMock()
    challenge.id = "c-1"
    challenge.period_type = "daily"
    challenge.period_end = datetime(2026, 4, 21, tzinfo=timezone.utc)
    challenge.round_id = "ancient-temple"
    challenge.max_attempts = 3

    app.dependency_overrides[get_current_user] = lambda: UserResponse(
        id="u1", email="u1@example.com", name="User One",
    )
    app.dependency_overrides[get_db_session] = lambda: MagicMock()

    try:
        with patch.object(view_module, "get_or_create_current_challenge", return_value=challenge), \
             patch.object(view_module, "get_round_by_id", return_value={
                 "id": "ancient-temple",
                 "title": "Ancient Temple",
                 "difficulty": "medium",
                 "reference_image": "ancient-temple.jpg",
             }), \
             patch.object(view_module, "get_user_challenge_progress", return_value=(1, 55.0)):
            client = TestClient(app)
            response = client.get(
                "/challenge/current",
                headers={"Authorization": "Bearer test-token"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["challenge_id"] == "c-1"
    assert payload["round_id"] == "ancient-temple"
    assert payload["title"] == "Ancient Temple"
    assert payload["attempts_used"] == 1
    assert payload["best_score"] == 55.0
