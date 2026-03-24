from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.main import app
from app.round.transport.get_db_session import get_db_session


def test_start_route_requires_bearer_token():
    client = TestClient(app)
    response = client.post("/round/start")
    assert response.status_code == 401
    body = response.json()
    assert body["error"] is not None


def test_start_route_returns_payload_with_authenticated_user():
    client = TestClient(app)
    app.dependency_overrides[get_current_user] = lambda: UserResponse(
        id="u1",
        email="u1@example.com",
        name="User One",
    )
    app.dependency_overrides[get_db_session] = lambda: MagicMock()

    response = client.post("/round/start", headers={"Authorization": "Bearer test-token"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert "round_id" in payload["data"]
    assert "target_image_url" in payload["data"]
