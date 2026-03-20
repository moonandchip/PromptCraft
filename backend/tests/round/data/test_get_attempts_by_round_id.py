import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, create_autospec

from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from app.round.data.get_attempts_by_round_id import get_attempts_by_round_id


class TestGetAttemptsByRoundId(unittest.TestCase):
    def test_executes_joined_query_and_returns_ordered_attempt_tuples(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.all.return_value = [
            SimpleNamespace(
                attempt_number=1,
                prompt="first prompt",
                generated_image_url="https://example.com/first.png",
                similarity_score=41.5,
            ),
            SimpleNamespace(
                attempt_number=2,
                prompt="second prompt",
                generated_image_url="https://example.com/second.png",
                similarity_score=67.0,
            ),
        ]
        session.execute.return_value = execute_result

        attempts = get_attempts_by_round_id(session=session, user_id="u1", round_id="ancient-temple")

        self.assertEqual(
            attempts,
            [
                (1, "first prompt", "https://example.com/first.png", 41.5),
                (2, "second prompt", "https://example.com/second.png", 67.0),
            ],
        )
        session.execute.assert_called_once()
        statement = session.execute.call_args.args[0]
        self.assertIsInstance(statement, Select)
        compiled = statement.compile()
        self.assertIn("u1", compiled.params.values())
        self.assertIn("ancient-temple", compiled.params.values())
        self.assertIn("ORDER BY attempts.attempt_number ASC", str(compiled))

    def test_normalizes_nullable_similarity_scores_to_zero(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.all.return_value = [
            SimpleNamespace(
                attempt_number=3,
                prompt="fallback score prompt",
                generated_image_url="https://example.com/third.png",
                similarity_score=None,
            )
        ]
        session.execute.return_value = execute_result

        attempts = get_attempts_by_round_id(session=session, user_id="u1", round_id="golden-sunset")

        self.assertEqual(attempts, [(3, "fallback score prompt", "https://example.com/third.png", 0.0)])
