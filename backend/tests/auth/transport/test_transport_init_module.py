import unittest

from app.auth.transport import router
from app.auth.transport.router import router as router_impl


class TestTransportInitModule(unittest.TestCase):
    def test_transport_init_re_exports_router(self):
        self.assertIs(router, router_impl)
