import unittest

from app.round.service.get_round_by_id import get_round_by_id


class TestGetRoundById(unittest.TestCase):
    def test_returns_round_definition_when_found(self):
        result = get_round_by_id("ancient-temple")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "ancient-temple")

    def test_returns_none_when_not_found(self):
        result = get_round_by_id("missing-round")
        self.assertIsNone(result)
