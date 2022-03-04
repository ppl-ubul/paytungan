from injector import Binder, Module, singleton

from .interfaces import IUserAccessor, IFirebaseProvider
from .accessors import UserAccessor, FirebaseProvider
from .services import UserServices, AuthService


class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IUserAccessor, to=UserAccessor, scope=singleton)
        binder.bind(IFirebaseProvider, to=FirebaseProvider, scope=singleton)
        binder.bind(UserServices, to=UserServices, scope=singleton)
        binder.bind(AuthService, to=AuthService, scope=singleton)
