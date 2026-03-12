import unittest
from unittest.mock import MagicMock, create_autospec

from sqlalchemy.orm import Session

from app.round.data.save_round_start import save_round_start


class TestSaveRoundStart(unittest.TestCase):
    def test_inserts_with_target_columns_and_commits(self):
        session = create_autospec(Session, instance=True, spec_set=True)

        save_round_start(
            session=session,
            user_id="u1",
            round_id="ancient-temple",
            target_image_url="/static/ancient-temple.jpg",
        )

        self.assertEqual(session.execute.call_count, 1)
        self.assertEqual(session.commit.call_count, 1)
        session.rollback.assert_not_called()

    def test_falls_back_to_minimal_insert_when_extended_columns_fail(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        session.execute.side_effect = [Exception("unknown column"), MagicMock()]

        save_round_start(
            session=session,
            user_id="u1",
            round_id="ancient-temple",
            target_image_url="/static/ancient-temple.jpg",
        )

        self.assertEqual(session.execute.call_count, 2)
        self.assertEqual(session.commit.call_count, 1)
        session.rollback.assert_called_once_with()
