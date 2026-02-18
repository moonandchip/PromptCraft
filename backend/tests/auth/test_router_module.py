import unittest

from app.auth.router import router as module_router
from app.auth.transport.router import router as transport_router


class TestRouterModule(unittest.TestCase):
    def test_router_module_re_exports_transport_router(self):
        self.assertIs(module_router, transport_router)
