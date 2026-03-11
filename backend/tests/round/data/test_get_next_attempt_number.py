import unittest
from unittest.mock import MagicMock, create_autospec

from sqlalchemy.orm import Session

from app.round.data.get_next_attempt_number import get_next_attempt_number


class TestGetNextAttemptNumber(unittest.TestCase):
    def test_returns_one_based_next_attempt_number(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.scalar_one.return_value = 4
        session.execute.return_value = execute_result

        attempt_number = get_next_attempt_number(session=session, user_id="u1", image_id="img1")

        self.assertEqual(attempt_number, 5)
