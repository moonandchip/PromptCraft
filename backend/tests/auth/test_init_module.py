import unittest

from app.auth import router as init_router
from app.auth.router import router as module_router


class TestAuthInitModule(unittest.TestCase):
    def test_init_module_exports_router(self):
        self.assertIs(init_router, module_router)
