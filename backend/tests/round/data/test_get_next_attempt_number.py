import unittest
from unittest.mock import MagicMock, create_autospec

from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from app.round.data.get_next_attempt_number import get_next_attempt_number


class TestGetNextAttemptNumber(unittest.TestCase):
    def test_returns_one_based_next_attempt_number_from_max(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.scalar_one.return_value = 4
        session.execute.return_value = execute_result

        attempt_number = get_next_attempt_number(session=session, user_id="u1", round_id="golden-sunset")

        self.assertEqual(attempt_number, 5)
        session.execute.assert_called_once()
        statement = session.execute.call_args.args[0]
        self.assertIsInstance(statement, Select)
        compiled = statement.compile()
        self.assertIn("u1", compiled.params.values())
        self.assertIn("golden-sunset", compiled.params.values())
        self.assertIn("attempts.round_id", str(compiled))
        self.assertNotIn("attempts.image_id", str(compiled))

    def test_returns_one_when_round_has_no_attempts(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.scalar_one.return_value = None
        session.execute.return_value = execute_result

        attempt_number = get_next_attempt_number(session=session, user_id="u1", round_id="ancient-temple")

        self.assertEqual(attempt_number, 1)
