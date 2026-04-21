"""Pytest configuration for challenge tests.

Mirrors tests/round/conftest.py so heavy ML dependencies are stubbed
when not installed. This keeps imports of app.challenge.service.submit_challenge
(which transitively pulls clip_scoring) safe in lean dev environments.
"""

import sys
import types
from unittest.mock import MagicMock


def _register_stub(name: str) -> None:
    if name not in sys.modules:
        stub = types.ModuleType(name)
        stub.__getattr__ = lambda item: MagicMock()  # type: ignore[attr-defined]
        sys.modules[name] = stub


try:
    import torch  # noqa: F401
except ImportError:
    _register_stub("torch")
    _register_stub("torch.nn")
    _register_stub("torch.nn.functional")

try:
    import transformers  # noqa: F401
except ImportError:
    _register_stub("transformers")
