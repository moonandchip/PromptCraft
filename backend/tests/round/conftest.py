"""Pytest configuration for round tests.

Stubs out heavy ML dependencies (torch, transformers) if they are not
already installed so that unit tests can run in environments where
those packages are not present (e.g. a plain Python dev setup without
the full Poetry virtualenv).  In Docker/CI, where the packages ARE
installed by Poetry, the real modules are used instead.
"""

import sys
import types
from unittest.mock import MagicMock


def _register_stub(name: str) -> None:
    """Insert a minimal module stub for *name* only if not already present.

    The stub uses Python 3.7+ module ``__getattr__`` (PEP 562) so that
    ``from stub import AnythingAtAll`` returns a fresh MagicMock at
    import time without errors.
    """
    if name not in sys.modules:
        stub = types.ModuleType(name)
        # PEP 562: setting __getattr__ on a module makes attribute misses
        # fall through to this function instead of raising AttributeError.
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
