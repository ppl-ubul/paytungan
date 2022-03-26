from dataclasses import dataclass
from typing import List, Optional

from .models import Bill, SplitBill


@dataclass
class GetBillListSpec:
    user_ids: Optional[List[int]] = None
    bill_ids: Optional[List[int]] = None
    split_bill_ids: Optional[List[int]] = None


@dataclass
class GetBillListResult:
    bills: List[Bill]


@dataclass
class GetSplitBillListSpec:
    user_fund_ids: Optional[List[int]] = None
    bill_ids: Optional[List[int]] = None
    split_bill_ids: Optional[List[int]] = None


@dataclass
class GetSplitBillListResult:
    split_bills: List[SplitBill]
