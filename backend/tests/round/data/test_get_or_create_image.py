import unittest
from unittest.mock import MagicMock, create_autospec

from sqlalchemy.orm import Session

from app.round.data.get_or_create_image import get_or_create_image


class TestGetOrCreateImage(unittest.TestCase):
    def test_returns_existing_image_id_when_found(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.scalar_one_or_none.return_value = "existing-image-id"
        session.execute.return_value = execute_result

        image_id = get_or_create_image(session=session, reference_image="golden-sunset.jpeg", difficulty="easy")

        self.assertEqual(image_id, "existing-image-id")
        session.add.assert_not_called()

    def test_creates_new_image_when_not_found(self):
        session = create_autospec(Session, instance=True, spec_set=True)
        execute_result = MagicMock()
        execute_result.scalar_one_or_none.return_value = None
        session.execute.return_value = execute_result

        image_id = get_or_create_image(session=session, reference_image="golden-sunset.jpeg", difficulty="easy")

        self.assertIsInstance(image_id, str)
        session.add.assert_called_once()
        session.flush.assert_called_once_with()
