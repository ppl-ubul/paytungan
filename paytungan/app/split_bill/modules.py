from injector import Binder, Module, singleton

from .interfaces import IBillAccessor, ISplitBillAccessor
from .accessors import SplitBillAccessor, BillAccessor
from .services import SplitBillService, BillService


class SplitBillModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IBillAccessor, to=BillAccessor, scope=singleton)
        binder.bind(ISplitBillAccessor, to=SplitBillAccessor, scope=singleton)
        binder.bind(SplitBillService, to=SplitBillService, scope=singleton)
        binder.bind(BillService, to=BillService, scope=singleton)
