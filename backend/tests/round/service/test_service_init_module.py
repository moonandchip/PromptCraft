import unittest

from app.round.service import (
    GenerationError,
    compute_similarity_score,
    generate_image,
    get_round_by_id,
    get_round_attempts,
    get_rounds,
    start_round,
    submit_round,
)
from app.round.service.clip_scoring import compute_similarity_score as compute_similarity_score_impl
from app.round.service.get_round_by_id import get_round_by_id as get_round_by_id_impl
from app.round.service.get_round_attempts import get_round_attempts as get_round_attempts_impl
from app.round.service.get_rounds import get_rounds as get_rounds_impl
from app.round.service.generate_image import GenerationError as GenerationErrorImpl
from app.round.service.generate_image import generate_image as generate_image_impl
from app.round.service.start_round import start_round as start_round_impl
from app.round.service.submit_round import submit_round as submit_round_impl


class TestRoundServiceInitModule(unittest.TestCase):
    def test_service_init_re_exports_compute_similarity_score(self):
        self.assertIs(compute_similarity_score, compute_similarity_score_impl)

    def test_service_init_re_exports_generate_image(self):
        self.assertIs(generate_image, generate_image_impl)

    def test_service_init_re_exports_generation_error(self):
        self.assertIs(GenerationError, GenerationErrorImpl)

    def test_service_init_re_exports_get_round_by_id(self):
        self.assertIs(get_round_by_id, get_round_by_id_impl)

    def test_service_init_re_exports_get_round_attempts(self):
        self.assertIs(get_round_attempts, get_round_attempts_impl)

    def test_service_init_re_exports_get_rounds(self):
        self.assertIs(get_rounds, get_rounds_impl)

    def test_service_init_re_exports_start_round(self):
        self.assertIs(start_round, start_round_impl)

    def test_service_init_re_exports_submit_round(self):
        self.assertIs(submit_round, submit_round_impl)
