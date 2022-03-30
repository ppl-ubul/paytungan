from abc import ABC, abstractmethod
from typing import List, Optional

from .specs import (
    BillDomain,
    CreateSplitBillSpec,
    GetBillListSpec,
    GetSplitBillListSpec,
    CreateBillSpec,
)
from .models import SplitBill, Bill


class ISplitBillAccessor(ABC):
    @abstractmethod
    def get(self, bill_id: int) -> Optional[SplitBill]:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, spec: GetSplitBillListSpec) -> List[SplitBill]:
        raise NotImplementedError

    @abstractmethod
    def create(self, spec: CreateSplitBillSpec) -> SplitBill:
        raise NotImplementedError

    @abstractmethod
    def get_list_by_user(self, user_id: int) -> List[SplitBill]:
        raise NotImplementedError


class IBillAccessor(ABC):
    @abstractmethod
    def get(self, bill_id: int) -> Optional[Bill]:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, spec: GetBillListSpec) -> List[Bill]:
        raise NotImplementedError

    @abstractmethod
    def create(self, obj: BillDomain) -> Bill:
        raise NotImplementedError

    @abstractmethod
    def bulk_create(self, objs: List[BillDomain]) -> List[Bill]:
        raise NotImplementedError
