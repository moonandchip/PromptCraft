import unittest

from app.auth.data import get_internal_me, post_internal_login, post_register, request_auth_service
from app.auth.data.get_internal_me import get_internal_me as get_internal_me_impl
from app.auth.data.post_internal_login import post_internal_login as post_internal_login_impl
from app.auth.data.post_register import post_register as post_register_impl
from app.auth.data.request_auth_service import request_auth_service as request_auth_service_impl


class TestDataInitModule(unittest.TestCase):
    def test_data_init_re_exports(self):
        self.assertIs(get_internal_me, get_internal_me_impl)
        self.assertIs(post_internal_login, post_internal_login_impl)
        self.assertIs(post_register, post_register_impl)
        self.assertIs(request_auth_service, request_auth_service_impl)
