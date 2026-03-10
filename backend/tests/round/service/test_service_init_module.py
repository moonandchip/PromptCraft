import unittest

from app.round.service import GenerationError, compute_similarity_score, generate_image
from app.round.service.clip_scoring import compute_similarity_score as compute_similarity_score_impl
from app.round.service.generate_image import GenerationError as GenerationErrorImpl
from app.round.service.generate_image import generate_image as generate_image_impl


class TestRoundServiceInitModule(unittest.TestCase):
    def test_service_init_re_exports_compute_similarity_score(self):
        self.assertIs(compute_similarity_score, compute_similarity_score_impl)

    def test_service_init_re_exports_generate_image(self):
        self.assertIs(generate_image, generate_image_impl)

    def test_service_init_re_exports_generation_error(self):
        self.assertIs(GenerationError, GenerationErrorImpl)
