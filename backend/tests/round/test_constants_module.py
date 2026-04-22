import unittest

from app.round import constants


class TestRoundConstantsModule(unittest.TestCase):
    def test_router_prefix(self):
        self.assertEqual(constants.ROUTER_PREFIX, "/round")

    def test_router_tag(self):
        self.assertEqual(constants.ROUTER_TAG, "round")

    def test_leonardo_api_v1_base_url(self):
        self.assertEqual(
            constants.LEONARDO_API_V1_BASE_URL,
            "https://cloud.leonardo.ai/api/rest/v1",
        )

    def test_leonardo_api_v2_base_url(self):
        self.assertEqual(
            constants.LEONARDO_API_V2_BASE_URL,
            "https://cloud.leonardo.ai/api/rest/v2",
        )

    def test_leonardo_generations_path(self):
        self.assertEqual(constants.LEONARDO_GENERATIONS_PATH, "/generations")

    def test_leonardo_api_key_env_var(self):
        self.assertEqual(constants.LEONARDO_API_KEY_ENV_VAR, "LEONARDO_API_KEY")

    def test_generation_width_is_positive(self):
        self.assertGreater(constants.GENERATION_WIDTH, 0)

    def test_generation_height_is_positive(self):
        self.assertGreater(constants.GENERATION_HEIGHT, 0)

    def test_generation_num_images_is_positive(self):
        self.assertGreater(constants.GENERATION_NUM_IMAGES, 0)

    def test_poll_interval_is_positive(self):
        self.assertGreater(constants.POLL_INTERVAL_SECONDS, 0)

    def test_poll_max_attempts_is_positive(self):
        self.assertGreater(constants.POLL_MAX_ATTEMPTS, 0)

    def test_error_constants_are_strings(self):
        self.assertIsInstance(constants.ERR_NO_API_KEY, str)
        self.assertIsInstance(constants.ERR_GENERATION_FAILED, str)
        self.assertIsInstance(constants.ERR_GENERATION_TIMEOUT, str)
        self.assertIsInstance(constants.ERR_ROUND_NOT_FOUND, str)
        self.assertIsInstance(constants.ERR_GENERATION_API_ERROR, str)

    def test_rounds_list_is_not_empty(self):
        self.assertGreater(len(constants.ROUNDS), 0)

    def test_each_round_has_required_keys(self):
        for round_def in constants.ROUNDS:
            self.assertIn("id", round_def)
            self.assertIn("title", round_def)
            self.assertIn("difficulty", round_def)
            self.assertIn("reference_image", round_def)
            self.assertIn("target_prompt", round_def)

    def test_each_round_has_non_empty_target_prompt(self):
        for round_def in constants.ROUNDS:
            self.assertIsInstance(round_def["target_prompt"], str)
            self.assertGreater(len(round_def["target_prompt"]), 0)

    def test_round_ids_are_unique(self):
        ids = [r["id"] for r in constants.ROUNDS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_round_difficulties_are_valid(self):
        valid_difficulties = {"easy", "medium", "hard"}
        for round_def in constants.ROUNDS:
            self.assertIn(round_def["difficulty"], valid_difficulties)
