import unittest

from pydantic import ValidationError

from app.round.models import AttemptInfo, RoundInfo, StartRoundResponse, SubmitRequest, SubmitResponse


class TestSubmitRequest(unittest.TestCase):
    def test_valid_submit_request(self):
        req = SubmitRequest(round_id="ancient-temple", user_prompt="a beautiful ancient temple")
        self.assertEqual(req.round_id, "ancient-temple")
        self.assertEqual(req.user_prompt, "a beautiful ancient temple")

    def test_empty_round_id_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            SubmitRequest(round_id="", user_prompt="a valid prompt")

    def test_empty_user_prompt_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            SubmitRequest(round_id="some-round", user_prompt="")

    def test_round_id_exceeds_max_length_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            SubmitRequest(round_id="x" * 101, user_prompt="a valid prompt")

    def test_user_prompt_exceeds_max_length_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            SubmitRequest(round_id="some-round", user_prompt="x" * 2001)

    def test_round_id_at_max_length_is_valid(self):
        req = SubmitRequest(round_id="x" * 100, user_prompt="a valid prompt")
        self.assertEqual(len(req.round_id), 100)

    def test_user_prompt_at_max_length_is_valid(self):
        req = SubmitRequest(round_id="some-round", user_prompt="x" * 2000)
        self.assertEqual(len(req.user_prompt), 2000)


class TestSubmitResponse(unittest.TestCase):
    def test_default_similarity_score_is_zero(self):
        resp = SubmitResponse(generated_image_url="https://example.com/image.jpg")
        self.assertEqual(resp.similarity_score, 0.0)

    def test_explicit_similarity_score(self):
        resp = SubmitResponse(
            generated_image_url="https://example.com/image.jpg",
            similarity_score=75.5,
        )
        self.assertEqual(resp.similarity_score, 75.5)

    def test_generated_image_url_is_stored(self):
        url = "https://example.com/generated.jpg"
        resp = SubmitResponse(generated_image_url=url)
        self.assertEqual(resp.generated_image_url, url)

    def test_similarity_score_zero_boundary(self):
        resp = SubmitResponse(generated_image_url="https://example.com/img.jpg", similarity_score=0.0)
        self.assertEqual(resp.similarity_score, 0.0)

    def test_similarity_score_max_boundary(self):
        resp = SubmitResponse(generated_image_url="https://example.com/img.jpg", similarity_score=100.0)
        self.assertEqual(resp.similarity_score, 100.0)


class TestRoundInfo(unittest.TestCase):
    def test_round_info_fields(self):
        round_info = RoundInfo(
            id="golden-sunset",
            title="Golden Sunset",
            difficulty="easy",
            reference_image="golden-sunset.jpeg",
        )
        self.assertEqual(round_info.id, "golden-sunset")
        self.assertEqual(round_info.title, "Golden Sunset")
        self.assertEqual(round_info.difficulty, "easy")
        self.assertEqual(round_info.reference_image, "golden-sunset.jpeg")

    def test_round_info_missing_field_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            RoundInfo(id="golden-sunset", title="Golden Sunset", difficulty="easy")


class TestStartRoundResponse(unittest.TestCase):
    def test_start_round_response_fields(self):
        response = StartRoundResponse(
            round_id="ancient-temple",
            target_image_url="/static/ancient-temple.jpg",
        )
        self.assertEqual(response.round_id, "ancient-temple")
        self.assertEqual(response.target_image_url, "/static/ancient-temple.jpg")

    def test_start_round_response_missing_field_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            StartRoundResponse(round_id="ancient-temple")


class TestAttemptInfo(unittest.TestCase):
    def test_attempt_info_fields(self):
        attempt = AttemptInfo(
            attempt_number=2,
            prompt="A vivid sunset over mountains",
            generated_image_url="https://example.com/generated.png",
            similarity_score=88.5,
        )

        self.assertEqual(attempt.attempt_number, 2)
        self.assertEqual(attempt.prompt, "A vivid sunset over mountains")
        self.assertEqual(attempt.generated_image_url, "https://example.com/generated.png")
        self.assertEqual(attempt.similarity_score, 88.5)

    def test_attempt_number_must_be_positive(self):
        with self.assertRaises(ValidationError):
            AttemptInfo(
                attempt_number=0,
                prompt="prompt",
                generated_image_url="https://example.com/generated.png",
                similarity_score=10.0,
            )
