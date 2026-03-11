import unittest
from unittest.mock import create_autospec

from sqlalchemy.orm import Session

from app.round.data.save_prompt import save_prompt


class TestSavePrompt(unittest.TestCase):
    def test_creates_prompt_and_returns_id(self):
        session = create_autospec(Session, instance=True, spec_set=True)

        prompt_id = save_prompt(session=session, user_id="u1", image_id="img1", prompt_text="a prompt")

        self.assertIsInstance(prompt_id, str)
        session.add.assert_called_once()
        session.flush.assert_called_once_with()
