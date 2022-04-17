from dataclasses import dataclass
from typing import List, Optional
from paytungan.app.base.constants import BillStatus

from paytungan.app.base.specs import BaseDomain
from .models import Bill, SplitBill


@dataclass
class GroupSplitBillDomain(BaseDomain):
    name: str
    user_fund_id: int
    withdrawal_method: str
    withdrawal_number: int
    amount: int
    details: Optional[str] = None
    bills: Optional[Bill] = None


@dataclass
class BillDomain(BaseDomain):
    user_id: int
    split_bill_id: int
    amount: int
    status: str = BillStatus.PENDING.value
    user_name: Optional[str] = None
    details: Optional[str] = None


@dataclass
class SplitBillWithBillDomain:
    split_bill: SplitBill
    bill: Bill


@dataclass
class GetBillListSpec:
    user_ids: Optional[List[int]] = None
    bill_ids: Optional[List[int]] = None
    split_bill_ids: Optional[List[int]] = None


@dataclass
class GetBillListResult:
    bills: List[Bill]


@dataclass
class CreateBillSpec:
    user_id: int
    split_bill_id: int
    amount: int
    details: Optional[str] = None


@dataclass
class GetSplitBillListSpec:
    user_fund_id: Optional[int] = None
    user_id: Optional[int] = None
    name: Optional[str] = None
    bill_ids: Optional[List[int]] = None
    split_bill_ids: Optional[List[int]] = None


@dataclass
class GetSplitBillListResult:
    split_bills: List[SplitBill]


@dataclass
class CreateSplitBillSpec:
    name: str
    user_fund_id: int
    withdrawal_method: str
    withdrawal_number: str
    amount: int
    details: Optional[str] = None


@dataclass
class UserIdWithAmountBillDomain:
    user_id: int
    amount: int


@dataclass
class CreateGroupSplitBillSpec:
    name: str
    user_fund_id: int
    withdrawal_method: str
    withdrawal_number: str
    amount: int
    bills: List[UserIdWithAmountBillDomain]
    details: Optional[str] = None


@dataclass
class DeleteSplitBillSpec:
    user_fund_id: Optional[int] = None
    bill_ids: Optional[List[int]] = None
    split_bill_ids: Optional[List[int]] = None
