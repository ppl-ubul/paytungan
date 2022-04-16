from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from paytungan.app.base.specs import BaseDomain


@dataclass
class GetPaymentListSpec:
    bill_ids: List[int] = field(default_factory=list)
    user_id: Optional[int] = None
    status: Optional[str] = None


@dataclass
class PaymentDomain(BaseDomain):
    bill_id: str
    status: str
    method: str
    reference_no: str
    paid_at: Optional[datetime] = None
    number: Optional[str] = None


@dataclass
class CreatePaymentSpec:
    bill_id: int
    method: str
    status: str
    reference_no: str
