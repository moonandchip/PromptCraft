import unittest

from app.round.data import (
    get_next_attempt_number,
    get_or_create_image,
    get_or_create_user,
    save_attempt,
    save_prompt,
    save_submission,
)
from app.round.data.get_next_attempt_number import get_next_attempt_number as get_next_attempt_number_impl
from app.round.data.get_or_create_image import get_or_create_image as get_or_create_image_impl
from app.round.data.get_or_create_user import get_or_create_user as get_or_create_user_impl
from app.round.data.save_attempt import save_attempt as save_attempt_impl
from app.round.data.save_prompt import save_prompt as save_prompt_impl
from app.round.data.save_submission import save_submission as save_submission_impl


class TestRoundDataInitModule(unittest.TestCase):
    def test_data_init_re_exports_get_or_create_user(self):
        self.assertIs(get_or_create_user, get_or_create_user_impl)

    def test_data_init_re_exports_get_or_create_image(self):
        self.assertIs(get_or_create_image, get_or_create_image_impl)

    def test_data_init_re_exports_save_prompt(self):
        self.assertIs(save_prompt, save_prompt_impl)

    def test_data_init_re_exports_get_next_attempt_number(self):
        self.assertIs(get_next_attempt_number, get_next_attempt_number_impl)

    def test_data_init_re_exports_save_attempt(self):
        self.assertIs(save_attempt, save_attempt_impl)

    def test_data_init_re_exports_save_submission(self):
        self.assertIs(save_submission, save_submission_impl)
