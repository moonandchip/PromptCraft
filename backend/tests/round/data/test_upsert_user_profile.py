import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.round.data.entities import UserProfile
from app.round.data.upsert_user_profile import upsert_user_profile


def _session_with_email_lookup(result):
    """Returns a MagicMock session whose select-by-email `.scalar_one_or_none()`
    returns `result`. `session.get()` is left as a MagicMock — callers should
    configure it if the email lookup misses and the id lookup should match."""
    session = MagicMock()
    session.execute.return_value.scalar_one_or_none.return_value = result
    return session


class TestUpsertUserProfileEmailLookup(unittest.TestCase):
    def test_updates_last_seen_and_fills_empty_display_name(self):
        existing = MagicMock(spec=UserProfile)
        existing.id = "existing-user"
        existing.email = "user@example.com"
        existing.display_name = None
        existing.last_seen_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        session = _session_with_email_lookup(existing)

        returned_id = upsert_user_profile(
            session, user_id="existing-user", email="user@example.com",
        )

        self.assertEqual(returned_id, "existing-user")
        self.assertEqual(existing.display_name, "user")
        self.assertIsInstance(existing.last_seen_at, datetime)
        self.assertGreater(existing.last_seen_at, datetime(2024, 1, 1, tzinfo=timezone.utc))
        session.add.assert_not_called()
        session.flush.assert_called_once()

    def test_overrides_display_name_when_explicit_provided(self):
        existing = MagicMock(spec=UserProfile)
        existing.id = "existing-user"
        existing.email = "user@example.com"
        existing.display_name = "Old Name"
        existing.last_seen_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        session = _session_with_email_lookup(existing)

        upsert_user_profile(
            session, user_id="existing-user", email="user@example.com", display_name="New Name",
        )

        self.assertEqual(existing.display_name, "New Name")

    def test_preserves_existing_display_name_when_none_provided(self):
        existing = MagicMock(spec=UserProfile)
        existing.id = "existing-user"
        existing.email = "user@example.com"
        existing.display_name = "Keep This"
        existing.last_seen_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        session = _session_with_email_lookup(existing)

        upsert_user_profile(
            session, user_id="existing-user", email="user@example.com",
        )

        self.assertEqual(existing.display_name, "Keep This")


class TestUpsertUserProfileIdFallback(unittest.TestCase):
    def test_falls_back_to_id_lookup_when_email_not_found(self):
        existing = MagicMock(spec=UserProfile)
        existing.id = "u1"
        existing.email = "old@example.com"
        existing.display_name = "Old Name"
        existing.last_seen_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        session = _session_with_email_lookup(None)
        session.get.return_value = existing

        returned_id = upsert_user_profile(
            session, user_id="u1", email="updated@example.com", display_name="New Name",
        )

        self.assertEqual(returned_id, "u1")
        self.assertEqual(existing.email, "updated@example.com")
        self.assertEqual(existing.display_name, "New Name")
        self.assertIsInstance(existing.last_seen_at, datetime)
        session.get.assert_called_once_with(UserProfile, "u1")
        session.add.assert_not_called()
        session.flush.assert_called_once()

    def test_id_fallback_fills_empty_display_name_with_safe_default(self):
        existing = MagicMock(spec=UserProfile)
        existing.id = "u1"
        existing.email = "old@example.com"
        existing.display_name = None
        existing.last_seen_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        session = _session_with_email_lookup(None)
        session.get.return_value = existing

        upsert_user_profile(session, user_id="u1", email="lookup@example.com")

        self.assertEqual(existing.display_name, "lookup")


class TestUpsertUserProfileCreate(unittest.TestCase):
    def test_creates_new_profile_when_neither_lookup_finds_a_match(self):
        session = _session_with_email_lookup(None)
        session.get.return_value = None

        returned_id = upsert_user_profile(
            session, user_id="new-user", email="new@example.com", display_name="New User",
        )

        self.assertEqual(returned_id, "new-user")
        session.add.assert_called_once()
        added_profile = session.add.call_args[0][0]
        self.assertIsInstance(added_profile, UserProfile)
        self.assertEqual(added_profile.id, "new-user")
        self.assertEqual(added_profile.email, "new@example.com")
        self.assertEqual(added_profile.display_name, "New User")
        session.flush.assert_called_once()

    def test_new_profile_falls_back_to_email_prefix_for_display_name(self):
        session = _session_with_email_lookup(None)
        session.get.return_value = None

        upsert_user_profile(session, user_id="new-user", email="handle@example.com")

        added_profile = session.add.call_args[0][0]
        self.assertEqual(added_profile.display_name, "handle")
