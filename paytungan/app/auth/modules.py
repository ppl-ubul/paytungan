from injector import Binder, Module, singleton

from .interfaces import IUserAccessor, IUserServices
from .accessors import UserAccessor
from .services import UserServices


class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IUserAccessor, to=UserAccessor, scope=singleton)
        binder.bind(IUserServices, to=UserServices, scope=singleton)
