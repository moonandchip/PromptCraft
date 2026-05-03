import unittest
from unittest.mock import MagicMock

from app.round.data.upsert_user_profile import upsert_user_profile


def _session_returning_id(returned_id: str) -> MagicMock:
    """Returns a MagicMock session whose execute().scalar_one() returns the
    given id — matches the upsert RETURNING shape."""
    session = MagicMock()
    session.execute.return_value.scalar_one.return_value = returned_id
    return session


class TestUpsertUserProfile(unittest.TestCase):
    def test_returns_id_from_upsert_returning_clause(self):
        session = _session_returning_id("u1")

        returned_id = upsert_user_profile(
            session, user_id="u1", email="user@example.com",
        )

        self.assertEqual(returned_id, "u1")
        session.execute.assert_called_once()
        session.flush.assert_called_once()

    def test_uses_email_prefix_when_no_display_name_provided(self):
        session = _session_returning_id("u1")

        upsert_user_profile(session, user_id="u1", email="handle@example.com")

        # The compiled INSERT should carry display_name="handle" in its values.
        stmt = session.execute.call_args.args[0]
        compiled_params = stmt.compile().params
        self.assertEqual(compiled_params["display_name"], "handle")

    def test_uses_explicit_display_name_when_provided(self):
        session = _session_returning_id("u1")

        upsert_user_profile(
            session, user_id="u1", email="user@example.com", display_name="Alice",
        )

        stmt = session.execute.call_args.args[0]
        compiled_params = stmt.compile().params
        self.assertEqual(compiled_params["display_name"], "Alice")

    def test_executes_postgres_on_conflict_upsert(self):
        """The query must use INSERT ... ON CONFLICT so concurrent requests
        for the same user can't race into a UniqueViolation. Smoke test by
        compiling the statement and looking for the expected SQL fragments."""
        session = _session_returning_id("u1")

        upsert_user_profile(session, user_id="u1", email="user@example.com")

        stmt = session.execute.call_args.args[0]
        sql = str(stmt.compile(compile_kwargs={"literal_binds": False}))
        self.assertIn("INSERT INTO user_profiles", sql)
        self.assertIn("ON CONFLICT", sql)
        self.assertIn("RETURNING", sql)
