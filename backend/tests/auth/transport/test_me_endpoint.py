import unittest

from app.auth.models import UserResponse
from app.auth.transport.me import me_endpoint


class TestMeEndpointTransportFunction(unittest.TestCase):
    def test_me_endpoint_returns_current_user(self):
        current_user = UserResponse(id="u1", email="user@example.com", name="User")
        result = me_endpoint(current_user=current_user)
        self.assertEqual(result.id, "u1")
