from dataclasses import dataclass
from typing import List, Optional

from paytungan.app.base.specs import BaseDomain
from .models import Bill, SplitBill


@dataclass
class GroupSplitBillDomain(BaseDomain):
    name: str
    user_fund_id: int
    withdrawal_method: str
    withdrawal_number: int
    details: Optional[str] = None
    bills: Optional[Bill] = None


@dataclass
class BillDomain(BaseDomain):
    user_id: int
    split_bill_id: int
    status: Optional[str] = None
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
    details: Optional[str] = None


@dataclass
class CreateGroupSplitBillSpec:
    name: str
    user_fund_id: int
    withdrawal_method: str
    withdrawal_number: str
    user_ids: List[int] = None
    details: Optional[str] = None


@dataclass
class DeleteSplitBillSpec:
    user_fund_id: Optional[int] = None
    bill_ids: Optional[List[int]] = None
    split_bill_ids: Optional[List[int]] = None
