from django.test import TestCase
from unittest.mock import MagicMock

from paytungan.app.auth.specs import CreateUserSpec, GetUserListSpec

from .services import UserServices


class TestService(TestCase):
    def setUp(self) -> None:
        self.mock = MagicMock()
        self.user_service = UserServices(user_accessor=self.mock)

    def test_user_service_get(self):
        self.user_service.get(1)
        assert True

    def test_user_service_get_list(self):
        spec = GetUserListSpec(user_ids=[1], usernames=[])
        self.user_service.get_list(spec)
        assert True

    def test_user_service_register(self):
        spec = CreateUserSpec(username="aa", email="aaa", password="aaa")
        self.user_service.create_user(spec)
        assert True
