from typing import List, Optional
from injector import inject

from .models import Bill, SplitBill
from .interfaces import (
    IBillAccessor,
    ISplitBillAccessor,
)
from .specs import (
    CreateBillSpec,
    GetBillListSpec,
    GetSplitBillListSpec,
)


class BillService:
    @inject
    def __init__(self, bill_accessor: IBillAccessor) -> None:
        self.bill_accessor = bill_accessor

    def get_bill(self, bill_id: int) -> Optional[Bill]:
        return self.bill_accessor.get(bill_id)

    def get_bill_list(self, spec: GetBillListSpec) -> List[Bill]:
        return self.bill_accessor.get(spec)

    def create_bill(self, spec: CreateBillSpec) -> Bill:
        return self.bill_accessor.create(spec)


class SplitBillService:
    @inject
    def __init__(
        self,
        bill_accessor: IBillAccessor,
        split_bill_accessor: ISplitBillAccessor,
    ) -> None:
        self.bill_accessor = bill_accessor
        self.split_bill_accessor = split_bill_accessor

    def get_split_bill(self, split_bill_id: int) -> Optional[SplitBill]:
        return self.split_bill_accessor.get(split_bill_id)

    def get_split_bill_list(self, spec: GetSplitBillListSpec) -> Optional[SplitBill]:
        return self.split_bill_accessor.get(spec)
