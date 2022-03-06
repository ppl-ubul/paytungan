from injector import Binder, Module, singleton
from django.conf import settings

from paytungan.app.base.constants import Environment
from .interfaces import IUserAccessor, IFirebaseProvider
from .accessors import UserAccessor, FirebaseProvider, DummyFirebaseProvider
from .services import UserServices, AuthService


class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IUserAccessor, to=UserAccessor, scope=singleton)
        binder.bind(UserServices, to=UserServices, scope=singleton)
        binder.bind(AuthService, to=AuthService, scope=singleton)

        if settings.CURRENT_ENV == Environment.TEST:
            binder.bind(IFirebaseProvider, to=DummyFirebaseProvider, scope=singleton)
        else:
            binder.bind(IFirebaseProvider, to=FirebaseProvider, scope=singleton)
