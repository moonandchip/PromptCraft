import unittest

import app.round.data as round_data_module


class TestRoundDataInitModule(unittest.TestCase):
    def test_data_module_is_importable(self):
        self.assertIsNotNone(round_data_module)

    def test_data_module_has_no_unexpected_public_exports(self):
        """Data layer is reserved – __all__ should not be defined yet."""
        self.assertFalse(hasattr(round_data_module, "__all__"))
