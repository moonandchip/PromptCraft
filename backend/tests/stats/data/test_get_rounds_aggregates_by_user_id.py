import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, create_autospec

from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from app.stats.data.get_rounds_aggregates_by_user_id import get_rounds_aggregates_by_user_id


class TestGetRoundsAggregatesByUserId(unittest.TestCase):
    def test_executes_select_and_returns_normalized_tuple(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        result = MagicMock()
        result.one.return_value = SimpleNamespace(
            rounds_played=3,
            average_score=26.6666667,
            best_score=50,
        )
        session.execute.return_value = result

        aggregates = get_rounds_aggregates_by_user_id(session=session, user_id="u1")

        self.assertEqual(aggregates, (3, 26.6666667, 50.0))
        session.execute.assert_called_once()
        called_statement = session.execute.call_args.args[0]
        self.assertIsInstance(called_statement, Select)
        compiled = called_statement.compile()
        self.assertIn("u1", compiled.params.values())
        result.one.assert_called_once_with()

    def test_returns_zeros_when_result_contains_null_like_values(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        result = MagicMock()
        result.one.return_value = SimpleNamespace(
            rounds_played=None,
            average_score=None,
            best_score=None,
        )
        session.execute.return_value = result

        aggregates = get_rounds_aggregates_by_user_id(session=session, user_id="u1")

        self.assertEqual(aggregates, (0, 0.0, 0.0))
