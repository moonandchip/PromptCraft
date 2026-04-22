import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.round.service.prompt_feedback import generate_prompt_feedback


class TestGeneratePromptFeedback(unittest.TestCase):
    _REF_PATH = Path("/fake/reference.jpg")

    @patch("app.round.service.prompt_feedback.os.environ.get", return_value="")
    def test_returns_empty_list_when_api_key_missing(self, _mock_env):
        result = generate_prompt_feedback(self._REF_PATH, "a sunset", 42.0)
        self.assertEqual(result, [])

    @patch("app.round.service.prompt_feedback.OpenAI")
    @patch("app.round.service.prompt_feedback._encode_image_to_base64", return_value="abc123")
    @patch("app.round.service.prompt_feedback.os.environ.get")
    def test_returns_parsed_bullet_points(self, mock_env_get, _mock_b64, mock_openai_cls):
        mock_env_get.side_effect = lambda key, default="": {
            "OPENAI_API_KEY": "sk-test",
            "PROMPT_FEEDBACK_MODEL": "gpt-4.1-mini",
        }.get(key, default)

        mock_message = MagicMock()
        mock_message.content = (
            "- Add more detail about the golden sky colors.\n"
            "- Mention the silhouette of trees in the foreground.\n"
            "- Specify warm lighting and soft haze.\n"
        )
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_openai_cls.return_value.chat.completions.create.return_value = mock_response

        result = generate_prompt_feedback(self._REF_PATH, "a sunset", 42.0)

        self.assertEqual(len(result), 3)
        self.assertIn("golden sky", result[0])
        self.assertIn("silhouette", result[1])
        system_prompt = mock_openai_cls.return_value.chat.completions.create.call_args.kwargs[
            "messages"
        ][0]["content"]
        self.assertIn("At least 1 bullet point must be a general prompt-engineering tip", system_prompt)

    @patch("app.round.service.prompt_feedback.OpenAI")
    @patch("app.round.service.prompt_feedback._encode_image_to_base64", return_value="abc123")
    @patch("app.round.service.prompt_feedback.os.environ.get")
    def test_returns_empty_list_on_api_error(self, mock_env_get, _mock_b64, mock_openai_cls):
        mock_env_get.side_effect = lambda key, default="": {
            "OPENAI_API_KEY": "sk-test",
            "PROMPT_FEEDBACK_MODEL": "gpt-4.1-mini",
        }.get(key, default)

        mock_openai_cls.return_value.chat.completions.create.side_effect = Exception("API error")

        result = generate_prompt_feedback(self._REF_PATH, "a sunset", 42.0)
        self.assertEqual(result, [])

    @patch("app.round.service.prompt_feedback.OpenAI")
    @patch("app.round.service.prompt_feedback._encode_image_to_base64", return_value="abc123")
    @patch("app.round.service.prompt_feedback.os.environ.get")
    def test_handles_non_bullet_response(self, mock_env_get, _mock_b64, mock_openai_cls):
        mock_env_get.side_effect = lambda key, default="": {
            "OPENAI_API_KEY": "sk-test",
            "PROMPT_FEEDBACK_MODEL": "gpt-4.1-mini",
        }.get(key, default)

        mock_message = MagicMock()
        mock_message.content = "Try being more specific about colors and lighting."
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_openai_cls.return_value.chat.completions.create.return_value = mock_response

        result = generate_prompt_feedback(self._REF_PATH, "a sunset", 42.0)

        self.assertEqual(len(result), 1)
        self.assertIn("more specific", result[0])
