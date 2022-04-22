from injector import Binder, Module, singleton

from .interfaces import IPaymentAccessor, IXenditProvider
from .accessors import PaymentAccessor, XenditProvider
from .services import PaymentService


class PaymentModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IPaymentAccessor, to=PaymentAccessor, scope=singleton)
        binder.bind(PaymentService, to=PaymentService, scope=singleton)
        binder.bind(IXenditProvider, to=XenditProvider, scope=singleton)
