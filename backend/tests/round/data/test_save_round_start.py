import unittest
from unittest.mock import create_autospec

from sqlalchemy.orm import Session

from app.round.data.save_round_start import save_round_start
from app.stats.data.entities import Round


class TestSaveRoundStart(unittest.TestCase):
    def test_stages_round_entity_without_committing(self):
        session = create_autospec(Session, instance=True, spec_set=True)

        save_round_start(
            session=session,
            user_id="u1",
            round_id="ancient-temple",
            target_image_url="/static/ancient-temple.jpg",
        )

        session.add.assert_called_once()
        added_obj = session.add.call_args[0][0]
        self.assertIsInstance(added_obj, Round)
        self.assertEqual(added_obj.user_id, "u1")
        self.assertEqual(added_obj.round_id, "ancient-temple")
        self.assertEqual(added_obj.target_image_url, "/static/ancient-temple.jpg")
        self.assertEqual(added_obj.score, 0.0)
        session.flush.assert_called_once()
        session.commit.assert_not_called()

    def test_propagates_db_errors(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        session.flush.side_effect = Exception("FK violation")

        with self.assertRaises(Exception, msg="FK violation"):
            save_round_start(
                session=session,
                user_id="u1",
                round_id="ancient-temple",
                target_image_url="/static/ancient-temple.jpg",
            )
