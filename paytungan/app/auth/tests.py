# from django.test import TestCase
from unittest import TestCase
from unittest.mock import MagicMock
from paytungan.app.auth.models import User

from paytungan.app.auth.specs import (
    CreateUserSpec,
    FirebaseDecodedToken,
    GetUserListSpec,
    UpdateUserSpec,
)

from .services import AuthService, UserServices


class TestService(TestCase):
    def setUp(self) -> None:
        self.mock = MagicMock()
        self.user_service = UserServices(user_accessor=self.mock)
        self.auth_service = AuthService(
            user_accessor=self.mock,
            firebase_provider=self.mock,
        )

    def test_user_service_get(self):
        self.user_service.get(1)
        assert True

    def test_user_service_get_list(self):
        spec = GetUserListSpec(user_ids=[1], usernames=[])
        self.user_service.get_list(spec)
        assert True

    def test_user_service_register(self):
        spec = CreateUserSpec(firebase_uid="aa", phone_number="aaa")
        self.user_service.create_user(spec)
        assert True

    def test_auth_login_succeed(self):
        token = "token"
        decode_token_return = FirebaseDecodedToken(
            user_id="342dwsdsd", phone_number="+62"
        )
        dummy_user = User(firebase_uid="342dwsdsd", phone_number="+62")

        self.mock.get_list.return_value = [dummy_user]
        self.mock.decode_token.return_value = decode_token_return

        user = self.auth_service.login(token)

        self.assertEqual(user.firebase_uid, dummy_user.firebase_uid)

    def test_auth_login_create_new_user(self):
        token = "token"
        decode_token_return = FirebaseDecodedToken(
            user_id="342dwsdsd", phone_number="+62"
        )
        dummy_user = User(firebase_uid="342dwsdsd", phone_number="+62")

        self.mock.create_user.return_value = dummy_user
        self.mock.get_list.return_value = []
        self.mock.decode_token.return_value = decode_token_return

        user = self.auth_service.login(token)

        self.assertEqual(user.firebase_uid, dummy_user.firebase_uid)

    def test_user_service_update_user(self):
        spec = UpdateUserSpec(firebase_uid="aa", username="aaa", name="aaaa", profil_image="aaaaa")
        self.user_service.update_user(spec)
        assert True