from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from xendit import Invoice

from paytungan.app.base.constants import PaymentStatus
from paytungan.app.base.specs import BaseDomain
from .models import Bill


@dataclass
class GetPaymentListSpec:
    bill_ids: List[int] = field(default_factory=list)
    user_id: Optional[int] = None
    status: Optional[str] = None


@dataclass
class PaymentDomain(BaseDomain):
    bill_id: int
    status: str = PaymentStatus.PENDING.value
    method: Optional[str] = None
    reference_no: Optional[str] = None
    paid_at: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    amount: Optional[str] = None
    number: Optional[str] = None
    payment_url: Optional[str] = None
    invoice: Optional[Invoice] = None


@dataclass
class CreatePaymentSpec:
    bill_id: int
    success_redirect_url: Optional[str] = None
    failure_redirect_url: Optional[str] = None


@dataclass
class UpdatePaymentSpec:
    obj: PaymentDomain
    updated_fields: Optional[List[str]] = None


@dataclass
class InvoiceDomain:
    id: str
    description: str
    invoice_url: str
    expiry_date: datetime
    status: str
    amount: int
    payment_method: Optional[str] = None
    paid_amount: Optional[int] = None
    payer_email: Optional[str] = None
    paid_at: Optional[datetime] = None
    success_redirect_url: Optional[str] = None
    failure_redirect_url: Optional[str] = None


@dataclass
class PayoutDomain:
    id: str
    external_id: str
    amount: int
    status: str
    expiration_timestamp: datetime
    created: datetime
    email: str
    payout_url: str


@dataclass
class CreateXenditInvoiceSpec:
    external_id: str
    amount: int
    payer_email: str
    description: str
    success_redirect_url: Optional[str] = None
    failure_redirect_url: Optional[str] = None


@dataclass
class UpdateStatusSpec:
    bill_id: int


@dataclass
class PaymentWithBillDomain:
    payment: PaymentDomain
    bill: Bill


@dataclass
class CreateInvoicePaymentSpec:
    payment_id: int
    payer_email: str
    success_redirect_url: Optional[str] = None
    failure_redirect_url: Optional[str] = None


@dataclass
class CreateInvoicePaymentResult:
    payment: PaymentDomain
    invoice: InvoiceDomain


@dataclass
class CreateXenditPayoutSpec:
    external_id: str
    amount: int
    email: str


@dataclass
class CreatePayoutSpec:
    split_bill_id: str


@dataclass
class CreatePayoutResult:
    payout: PayoutDomain
