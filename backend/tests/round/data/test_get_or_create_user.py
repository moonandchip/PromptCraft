import unittest
from unittest.mock import MagicMock, create_autospec, patch

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.round.data.get_or_create_user import get_or_create_user


class TestGetOrCreateUser(unittest.TestCase):
    def test_returns_existing_user_id_when_found(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.scalar_one_or_none.return_value = "existing-user-id"
        session.execute.return_value = execute_result

        user_id = get_or_create_user(session=session, email="test@example.com")

        self.assertEqual(user_id, "existing-user-id")
        session.add.assert_not_called()

    def test_creates_new_user_when_not_found(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.scalar_one_or_none.return_value = None
        session.execute.return_value = execute_result

        user_id = get_or_create_user(session=session, email="test@example.com")

        self.assertIsInstance(user_id, str)
        session.add.assert_called_once()
        session.flush.assert_called_once_with()

    @patch("app.round.data.get_or_create_user.select", autospec=True)
    def test_handles_integrity_error_by_refetching_user_id(self, mock_select):
        session = create_autospec(Session, instance=True, spec_set=True)
        first_execute = MagicMock()
        first_execute.scalar_one_or_none.return_value = None
        second_execute = MagicMock()
        second_execute.scalar_one.return_value = "race-winner-id"
        session.execute.side_effect = [first_execute, second_execute]
        session.flush.side_effect = IntegrityError("insert", {}, Exception("duplicate"))
        mock_select.return_value = MagicMock()

        user_id = get_or_create_user(session=session, email="test@example.com")

        self.assertEqual(user_id, "race-winner-id")
        session.rollback.assert_called_once_with()
