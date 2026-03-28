import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from app.round.data.entities import UserProfile
from app.round.data.upsert_user_profile import upsert_user_profile


class TestUpsertUserProfile(unittest.TestCase):
    def test_creates_new_profile_when_user_does_not_exist(self):
        session = MagicMock()
        session.get.return_value = None

        upsert_user_profile(session, user_id="new-user", email="new@example.com", display_name="New User")

        session.add.assert_called_once()
        added_profile = session.add.call_args[0][0]
        self.assertIsInstance(added_profile, UserProfile)
        self.assertEqual(added_profile.id, "new-user")
        self.assertEqual(added_profile.email, "new@example.com")
        self.assertEqual(added_profile.display_name, "New User")
        session.flush.assert_called_once()

    def test_creates_new_profile_without_display_name(self):
        session = MagicMock()
        session.get.return_value = None

        upsert_user_profile(session, user_id="new-user", email="new@example.com")

        session.add.assert_called_once()
        added_profile = session.add.call_args[0][0]
        self.assertIsNone(added_profile.display_name)
        session.flush.assert_called_once()

    def test_updates_existing_profile_email_and_last_seen(self):
        existing = MagicMock(spec=UserProfile)
        existing.email = "old@example.com"
        existing.display_name = "Old Name"
        existing.last_seen_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        session = MagicMock()
        session.get.return_value = existing

        upsert_user_profile(session, user_id="existing-user", email="updated@example.com", display_name="New Name")

        self.assertEqual(existing.email, "updated@example.com")
        self.assertEqual(existing.display_name, "New Name")
        self.assertIsInstance(existing.last_seen_at, datetime)
        session.add.assert_not_called()
        session.flush.assert_called_once()

    def test_update_preserves_existing_display_name_when_none_provided(self):
        existing = MagicMock(spec=UserProfile)
        existing.email = "old@example.com"
        existing.display_name = "Keep This"
        existing.last_seen_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        session = MagicMock()
        session.get.return_value = existing

        upsert_user_profile(session, user_id="existing-user", email="updated@example.com", display_name=None)

        self.assertEqual(existing.display_name, "Keep This")
        session.flush.assert_called_once()

    def test_looks_up_user_by_id(self):
        session = MagicMock()
        session.get.return_value = None

        upsert_user_profile(session, user_id="lookup-user", email="lookup@example.com")

        session.get.assert_called_once_with(UserProfile, "lookup-user")
