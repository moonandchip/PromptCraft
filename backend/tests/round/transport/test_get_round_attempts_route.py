from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.auth.constants import ERR_MISSING_BEARER_TOKEN
from app.auth.dependencies import get_current_user
from app.auth.models import UserResponse
from app.main import app
from app.round.transport.get_db_session import get_db_session


def test_get_round_attempts_route_requires_bearer_token():
    client = TestClient(app)

    response = client.get("/round/ancient-temple/attempts")

    assert response.status_code == 401
    assert response.json()["detail"] == ERR_MISSING_BEARER_TOKEN


def test_get_round_attempts_route_returns_attempts_for_authenticated_user():
    client = TestClient(app)
    app.dependency_overrides[get_current_user] = lambda: UserResponse(
        id="u1",
        email="u1@example.com",
        name="User One",
    )
    app.dependency_overrides[get_db_session] = lambda: MagicMock()

    with patch(
        "app.round.transport.get_round_attempts_endpoint.get_round_attempts",
        autospec=True,
    ) as mock_get_round_attempts:
        mock_get_round_attempts.return_value = [
            {
                "attempt_number": 1,
                "prompt": "first prompt",
                "generated_image_url": "https://example.com/first.png",
                "similarity_score": 54.0,
            }
        ]
        response = client.get(
            "/round/ancient-temple/attempts",
            headers={"Authorization": "Bearer test-token"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [
        {
            "attempt_number": 1,
            "prompt": "first prompt",
            "generated_image_url": "https://example.com/first.png",
            "similarity_score": 54.0,
        }
    ]
