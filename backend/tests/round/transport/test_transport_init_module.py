import unittest

from app.round.transport import router as init_router
from app.round.transport.router import router as module_router


class TestRoundTransportInitModule(unittest.TestCase):
    def test_transport_init_re_exports_router(self):
        self.assertIs(init_router, module_router)
