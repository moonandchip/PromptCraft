import unittest

from pydantic import ValidationError

from app.challenge.models import (
    ChallengeStateResponse,
    ChallengeSubmitRequest,
    ChallengeSubmitResponse,
    LeaderboardEntry,
    LeaderboardResponse,
)


class TestChallengeSubmitRequest(unittest.TestCase):
    def test_valid_request(self):
        req = ChallengeSubmitRequest(user_prompt="a vivid scene")
        self.assertEqual(req.user_prompt, "a vivid scene")

    def test_empty_prompt_raises(self):
        with self.assertRaises(ValidationError):
            ChallengeSubmitRequest(user_prompt="")

    def test_prompt_max_length_boundary(self):
        req = ChallengeSubmitRequest(user_prompt="x" * 2000)
        self.assertEqual(len(req.user_prompt), 2000)

    def test_prompt_exceeding_max_length_raises(self):
        with self.assertRaises(ValidationError):
            ChallengeSubmitRequest(user_prompt="x" * 2001)


class TestChallengeStateResponse(unittest.TestCase):
    def test_full_payload(self):
        state = ChallengeStateResponse(
            challenge_id="c-1",
            period_type="daily",
            period_end="2026-04-21T00:00:00+00:00",
            round_id="r1",
            title="Round One",
            difficulty="easy",
            target_image_url="/static/r1.jpg",
            max_attempts=3,
            attempts_used=1,
            best_score=42.5,
        )
        self.assertEqual(state.attempts_used, 1)
        self.assertEqual(state.best_score, 42.5)

    def test_default_best_score_is_zero(self):
        state = ChallengeStateResponse(
            challenge_id="c-1",
            period_type="daily",
            period_end="2026-04-21T00:00:00+00:00",
            round_id="r1",
            title="Round One",
            difficulty="easy",
            target_image_url="/static/r1.jpg",
            max_attempts=3,
            attempts_used=0,
        )
        self.assertEqual(state.best_score, 0.0)

    def test_missing_field_raises(self):
        with self.assertRaises(ValidationError):
            ChallengeStateResponse(challenge_id="c-1")


class TestChallengeSubmitResponse(unittest.TestCase):
    def test_full_payload(self):
        resp = ChallengeSubmitResponse(
            generated_image_url="https://example.com/x.jpg",
            similarity_score=85.0,
            attempts_used=2,
            attempts_remaining=1,
            best_score=85.0,
        )
        self.assertEqual(resp.attempts_remaining, 1)

    def test_defaults(self):
        resp = ChallengeSubmitResponse(
            generated_image_url="https://example.com/x.jpg",
            attempts_used=0,
            attempts_remaining=3,
        )
        self.assertEqual(resp.similarity_score, 0.0)
        self.assertEqual(resp.best_score, 0.0)


class TestLeaderboardModels(unittest.TestCase):
    def test_leaderboard_entry(self):
        entry = LeaderboardEntry(
            rank=1,
            user_id="u1",
            display_name="Alice",
            best_score=92.0,
            attempts_used=2,
        )
        self.assertEqual(entry.rank, 1)
        self.assertEqual(entry.display_name, "Alice")

    def test_leaderboard_response_accepts_empty_entries(self):
        resp = LeaderboardResponse(
            challenge_id="c-1",
            period_end="2026-04-21T00:00:00+00:00",
            entries=[],
        )
        self.assertEqual(resp.entries, [])

    def test_leaderboard_response_carries_entries(self):
        resp = LeaderboardResponse(
            challenge_id="c-1",
            period_end="2026-04-21T00:00:00+00:00",
            entries=[
                LeaderboardEntry(rank=1, user_id="u1", display_name="A", best_score=90.0, attempts_used=1),
                LeaderboardEntry(rank=2, user_id="u2", display_name="B", best_score=80.0, attempts_used=2),
            ],
        )
        self.assertEqual(len(resp.entries), 2)
        self.assertEqual(resp.entries[1].user_id, "u2")
