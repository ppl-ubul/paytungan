from injector import Binder, Module, singleton

from .interface import ILoggingProvider
from .adapters import LoggingProvider


class LoggingModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            ILoggingProvider,
            to=LoggingProvider,
            scope=singleton,
        )
