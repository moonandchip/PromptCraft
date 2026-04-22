import unittest

from app.challenge.exceptions import (
    ChallengeError,
    GetCurrentChallengeException,
    GetLeaderboardException,
    SubmitChallengeException,
)


class TestChallengeError(unittest.TestCase):
    def test_known_codes_present(self):
        self.assertEqual(ChallengeError.NOT_FOUND.value, "CHALLENGE_NOT_FOUND")
        self.assertEqual(ChallengeError.ATTEMPT_LIMIT_REACHED.value, "CHALLENGE_ATTEMPT_LIMIT_REACHED")
        self.assertEqual(ChallengeError.GENERATION_FAILED.value, "CHALLENGE_GENERATION_FAILED")
        self.assertEqual(ChallengeError.GENERATION_TIMEOUT.value, "CHALLENGE_GENERATION_TIMEOUT")
        self.assertEqual(ChallengeError.SAVE_FAILED.value, "CHALLENGE_SAVE_FAILED")


class TestGetCurrentChallengeException(unittest.TestCase):
    def test_not_found_maps_to_404(self):
        exc = GetCurrentChallengeException(ChallengeError.NOT_FOUND)
        self.assertEqual(exc.status_code, 404)

    def test_unknown_default_is_500(self):
        exc = GetCurrentChallengeException()
        self.assertEqual(exc.status_code, 500)


class TestSubmitChallengeException(unittest.TestCase):
    def test_attempt_limit_maps_to_429(self):
        exc = SubmitChallengeException(ChallengeError.ATTEMPT_LIMIT_REACHED)
        self.assertEqual(exc.status_code, 429)

    def test_generation_failed_maps_to_502(self):
        exc = SubmitChallengeException(ChallengeError.GENERATION_FAILED)
        self.assertEqual(exc.status_code, 502)

    def test_generation_timeout_maps_to_504(self):
        exc = SubmitChallengeException(ChallengeError.GENERATION_TIMEOUT)
        self.assertEqual(exc.status_code, 504)

    def test_not_found_maps_to_404(self):
        exc = SubmitChallengeException(ChallengeError.NOT_FOUND)
        self.assertEqual(exc.status_code, 404)

    def test_save_failed_maps_to_500(self):
        exc = SubmitChallengeException(ChallengeError.SAVE_FAILED)
        self.assertEqual(exc.status_code, 500)

    def test_message_passthrough(self):
        exc = SubmitChallengeException(ChallengeError.NOT_FOUND, message="missing")
        self.assertEqual(exc.message, "missing")


class TestGetLeaderboardException(unittest.TestCase):
    def test_default_status_500(self):
        exc = GetLeaderboardException()
        self.assertEqual(exc.status_code, 500)
