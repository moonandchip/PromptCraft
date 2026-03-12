import unittest
from unittest.mock import patch

from app.stats.transport.get_db_session import get_db_session


class TestGetDbSessionTransportDependency(unittest.TestCase):
    @patch("app.stats.transport.get_db_session.app_get_db_session", autospec=True)
    def test_yields_from_shared_app_db_dependency(self, mock_app_get_db_session):
        sentinel_session = object()
        mock_app_get_db_session.return_value = iter([sentinel_session])

        generator = get_db_session()
        yielded = next(generator)

        self.assertIs(yielded, sentinel_session)
        with self.assertRaises(StopIteration):
            next(generator)
        mock_app_get_db_session.assert_called_once_with()
