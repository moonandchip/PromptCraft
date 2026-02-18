import io
import unittest
from urllib import error
from unittest.mock import patch

from tests.auth._common import MockHTTPResponse

from app.auth.data.request_auth_service import request_auth_service
from app.auth.service.errors import AuthServiceError


class TestRequestAuthService(unittest.TestCase):
    @patch("app.auth.data.request_auth_service.request.urlopen")
    def test_request_auth_service_success(self, mock_urlopen):
        mock_urlopen.return_value = MockHTTPResponse({"access_token": "abc"})
        result = request_auth_service(
            method="POST",
            path="/api/internal/login",
            base_url="http://auth.test",
            timeout_seconds=10.0,
            body={"email": "user@example.com", "password": "strongpass123"},
        )
        self.assertEqual(result["access_token"], "abc")

    @patch("app.auth.data.request_auth_service.request.urlopen")
    def test_request_auth_service_rejects_non_dict(self, mock_urlopen):
        mock_urlopen.return_value = MockHTTPResponse(["invalid"])
        with self.assertRaises(AuthServiceError) as exc:
            request_auth_service(
                method="GET",
                path="/api/internal/me",
                base_url="http://auth.test",
                timeout_seconds=10.0,
            )
        self.assertEqual(exc.exception.status_code, 502)

    @patch("app.auth.data.request_auth_service.request.urlopen")
    def test_request_auth_service_maps_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = error.HTTPError(
            url="http://auth.test/api/internal/login",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b'{"error":"Invalid credentials"}'),
        )
        with self.assertRaises(AuthServiceError) as exc:
            request_auth_service(
                method="POST",
                path="/api/internal/login",
                base_url="http://auth.test",
                timeout_seconds=10.0,
                body={"email": "user@example.com", "password": "wrongpass123"},
            )
        self.assertEqual(exc.exception.status_code, 401)
        self.assertEqual(exc.exception.detail, "Invalid credentials")

    @patch("app.auth.data.request_auth_service.request.urlopen")
    def test_request_auth_service_maps_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = error.URLError("connection failed")
        with self.assertRaises(AuthServiceError) as exc:
            request_auth_service(
                method="GET",
                path="/api/internal/me",
                base_url="http://auth.test",
                timeout_seconds=10.0,
            )
        self.assertEqual(exc.exception.status_code, 503)
