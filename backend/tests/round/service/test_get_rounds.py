import unittest

from app.round.models import RoundInfo
from app.round.service.get_rounds import get_rounds


class TestGetRounds(unittest.TestCase):
    def test_returns_round_info_list(self):
        result = get_rounds()
        self.assertIsInstance(result, list)
        self.assertTrue(result)
        self.assertIsInstance(result[0], RoundInfo)
