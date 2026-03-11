import unittest

from app.round import router as init_router
from app.round.transport.router import router as module_router


class TestRoundInitModule(unittest.TestCase):
    def test_init_module_exports_router(self):
        self.assertIs(init_router, module_router)
